import itertools
import multiprocessing as mp
import logging
import numpy as np
import os
import re
import time

from datetime import datetime
from bs4 import BeautifulSoup
from pywikiapi import wikipedia


class Corpus:
    def __init__(
        self,
        lang,
        max_size=-1,
        random_choise=False,
        min_len=None,
        max_len=None,
        verbose=10,
        merge=False,
        filter_latex=True,
        filter_punctuation=False,
        custom_filters=[],
    ):
        self.size = 0
        self.lang = lang
        self.generator = iter([])
        self.max_size = max_size
        self.random_choise = random_choise
        self.site = wikipedia(self.lang)
        self.min_len = min_len
        self.max_len = max_len
        self.verbose = verbose
        self.merge = merge
        self.filter_latex = filter_latex
        self.filter_punctuation = filter_punctuation

        self.last_actions = []

        self.custom_filters = custom_filters
        self.latex_filters = [
            "\\\w+",  # latex insertions like \displaystyle, \log, \over, \epsilon, etc.
        ]
        self.punctuation_filters = [
            "(\.\s*){4,}",  # more than 3 dots in a row
            "\.\s*\.\s*[!?\-,:;]"  # exactly 2 dots in a row and inappropriate punctuation symbol after
            "(\?\s*){4,}",  # more than 3 question marks in a row
            "(!\s*){4,}",  # more than 3 exclamation points in a row
            "(\,\s*){2,}",  # more than 2 commas in a row
            "[,:;\-!?]\s*\.",  # dot after other punctuantion symbol
        ]

        filters = []
        if self.filter_latex:
            filters += self.latex_filters
        if self.filter_punctuation:
            filters += self.punctuation_filters

        try:
            if 0 == len(filters) + len(self.custom_filters):
                self.filter = None
            else:
                self.filter = re.compile("|".join(filters + self.custom_filters))
        except Exception:
            logging.warn(f"failed to load custom filters - ignoring...")
            if 0 == len(filters):
                self.filter = None
            else:
                self.filter = re.compile("|".join(filters))

    def __len__(self):
        return self.size

    def __iterate_wikipages_by_id__(self, pageids):
        paragaraphs = []
        for pageid in pageids:
            logging.info(f"proccessing page with id {pageid}")
            self.last_actions.append(pageid)
            if self.verbose > 0 and len(self.last_actions) >= self.verbose:
                print(
                    f"Processed pages with IDs: {','.join(map(str, self.last_actions))}"
                )
                self.last_actions = []

            gen = self.site.query(
                pageids=pageid, prop=["extracts"], exlimit=1
            )  # could use explaintext instead bs4 html parser
            try:
                info = next(gen)
                page = info["pages"][0]
                html_text = page["extract"].replace("\xa0", " ").replace("\n", "")
                soup = BeautifulSoup(html_text, "html.parser")
                paragaraph = ""
                l = 0
                for data in soup.find_all("p"):
                    new_paragraph = data.get_text()
                    paragaraph += new_paragraph
                    l += len(new_paragraph.split())
                    if self.filter is not None:  # if filtering is defined
                        if (
                            self.filter.search(paragaraph) is not None
                        ):  # if some of filters have triggered
                            paragaraph = ""
                            l = 0
                            continue
                    # merging case
                    if self.min_len is not None and l < self.min_len:
                        if not self.merge:
                            paragaraph = ""
                            l = 0
                        continue
                    # no splitting case due to inabillity to split texts into sentences in a correct way
                    elif self.max_len is not None and l > self.max_len:
                        paragaraph = ""
                        l = 0
                        continue
                    else:
                        paragaraphs.append(paragaraph)
                        paragaraph = ""
                        l = 0

            except:
                continue
        if self.random_choise:
            paragaraphs = np.random.permutation(paragaraphs)

        return paragaraphs

    def collect_data(self, n_proc=os.cpu_count() - 1, prefix=""):
        print(f"Started collecting data using {n_proc} jobs...")
        start_time = datetime.now()
        corpus_gens = []
        pages_gen = self.site.query(list="allpages", apprefix=prefix)
        with mp.Pool(n_proc) as pool:
            while True:
                batch = []
                while len(batch) < 2 * n_proc:
                    try:
                        pages = next(pages_gen)
                        pageids = [page.pageid for page in pages.allpages]
                        batch.append(pageids)
                    except StopIteration:
                        break

                res = pool.starmap(
                    Corpus.__iterate_wikipages_by_id__,
                    zip(itertools.repeat(self), batch),
                )
                for paragaraph in res:
                    self.size += len(paragaraph)
                    corpus_gens.append(iter(paragaraph))

                if self.size >= self.max_size:
                    break

        self.generator = itertools.chain(*corpus_gens)

        if self.max_size > 0:
            self.generator = itertools.islice(self.generator, self.max_size)
            self.size = self.max_size

        end_time = datetime.now()
        print(
            f"Finished collecting data from wikipages.\nProcessing time: {end_time - start_time}."
        )

    def reset_data(self):
        self.generator = iter([])
        self.size = 0

    def get_data(self):
        return self.generator

    def save_tsv(
        self, file_path=None, encoding="utf-8", write_len=False, skip_titles=False
    ):
        if file_path is None:
            timestamp_name = f"{int(time.time())}.tsv"
            file_path = os.path.join(os.curdir, timestamp_name)
        with open(file_path, "w", encoding=encoding) as target:
            if not skip_titles:
                target.write(f"INPUT:text_id\tINPUT:text\n")
            for ind, paragaraph in enumerate(self.generator):
                res_string = f"{ind}\t"
                if write_len:
                    res_string += f"{len(paragaraph)}\t"
                res_string += paragaraph
                res_string += "\n"
                target.write(res_string)
