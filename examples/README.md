# Toloka-kit usage examples
## _Data collection, markup, aggregation, and other applications_

Why it may be usefull:
- Easily reuse projects by just copying and pasting code. No need to configure parameters in the interface over and over again.
- Train your ML models and run your data labeling projects in the same environment.
- Take advantage of open-source code that anyone can use and contribute to.

## Table of content

| Example | Abstract | Key words |
| ------ | ------ | ------ |
| [Learn the basics](https://github.com/Toloka/toloka-kit/tree/main/examples/0.getting_started/0.learn_the_basics) <br/><br/> [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Toloka/toloka-kit/blob/main/examples/0.getting_started/0.learn_the_basics/learn_the_basics.ipynb) | The very first example explains the basics of working with Toloka and toloka-kit. Everything is explained by the example of the project on the classification of cats and dogs. |```Getting Started```,  ```Classification```|
| [Object detection](https://github.com/Toloka/toloka-kit/tree/main/examples/1.computer_vision/object_detection) <br/><br/> [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Toloka/toloka-kit/blob/main/examples/1.computer_vision/object_detection/object_detection.ipynb) | Example of solving the classic problem of annotating images for training detection algorithms. In real-world tasks, annotation is usually done with a polygon. We chose to use a rectangular outline to simplify the task so that we can reduce costs and speed things up. |```CV```, ```Segmentation```,  ```Detection```, ```Bounding boxes```, ```Street```, ```Traffic sign```, ```Verification Project```|
| [Questing answering on SQuAD](https://github.com/Toloka/toloka-kit/tree/main/examples/SQUAD2.0) <br/><br/> [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Toloka/toloka-kit/blob/main/examples/SQUAD2.0/SQUAD2.0_processing.ipynb) | Solving the problem of question answering on SQUAD2.0 dataset. Collects and validates answers for questions by human performers. One of the most popular tasks in natural language processing. | ```NLP```, ```Questing Answering```, ```Texts```, ```Benchmark```, ```Verification Project```|
| [Image collection](https://github.com/Toloka/toloka-kit/tree/main/examples/1.computer_vision/image_collection) <br/><br/> [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Toloka/toloka-kit/blob/main/examples/1.computer_vision/image_collection/image_collection.ipynb) | The goal for this project is to collect a dataset  of dogs' and cats' images. Performers will be asked to take a photo of their pet and specify its species. |```CV```,  ```Classification```, ```Collecting```, ```Dataset```|
| [Simplest Spatial Crowdsourcing](https://github.com/Toloka/toloka-kit/tree/main/examples/2.spatial_crowdsourcing/0.simplest_example) <br/><br/> [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Toloka/toloka-kit/blob/main/examples/2.spatial_crowdsourcing/0.simplest_example/spatial_crowdsourcing.ipynb) | In this example, we will collect pictures of the Moscow metro entrances. This example also can be reused for production tasks such as monitoring the state of objects, checking the presence of an organization or other physical object. |```Spatial Crowdsourcing```, ```Outdoor monitoring```, ```Collecting```|
| [ASR/TTS based on Wikipedia articles](https://github.com/noath/asr-datasets-pipeline) <br/><br/> [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/noath/asr-datasets-pipeline/blob/main/ASR_pipeline.ipynb) | This example contains full speech data collecting pipeline from extracting raw texts to labeling and validating speech records. | ```ASR```,  ```TTS```, ```Texts```, ```Verification project```, ```Audio samples collection```|
| [Blood cells classification](https://github.com/oleg-cat/blood-test/blob/main/blood-test.ipynb) <br/><br/> [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/oleg-cat/blood-test/blob/main/blood-test.ipynb) | In this project, we will show an image of a blood cell and a brief instruction for Toloka performers. Then, we will ask performers to choose which type of white blood cell they see on this image. | ```CV```,  ```Classification```, ```Medicine```, ```Benchmark```|

# Need more examples?
If you have an example of data labeling using toloka-kit, do not hesitate to send it. Add a link to your GitHub repository and a description to this table via a [pool request](https://github.com/Toloka/toloka-kit/pulls).

Ideally, a great example should contain the following aspects:
- Problem statement;
- How to set up a project;
- Where to get the data for the example;
- What to pay attention to when writing instructions;
- How to set up quality control;
- What is the final quality;
- Visualization of the obtained results;

You may also ask any question or ask for a new example using [issues](https://github.com/Toloka/toloka-kit/issues)
