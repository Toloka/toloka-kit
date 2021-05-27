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
| [Image segmentation/detection](https://github.com/Toloka/toloka-kit/tree/main/examples/image_segmentation) <br/><br/> [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Toloka/toloka-kit/blob/main/examples/image_segmentation/image_segmentation.ipynb) | Example of solving the classic problem of annotating images for training segmentation algorithms. In real-world tasks, annotation is usually done with a polygon. We chose to use a rectangular outline to simplify the task so that we can reduce costs and speed things up. |```CV```, ```Segmentation```,  ```Detection```, ```Bounding boxes```, ```Street```, ```Traffic sign```, ```Verification Project```|
| [Questing answering on SQuAD](https://github.com/Toloka/toloka-kit/tree/main/examples/SQUAD2.0) <br/><br/> [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Toloka/toloka-kit/blob/main/examples/SQUAD2.0/SQUAD2.0_processing.ipynb) | Solving the problem of question answering on SQUAD2.0 dataset. Collects and validates answers for questions by human performers. One of the most popular tasks in natural language processing. | ```NLP```, ```Questing Answering```, ```Texts```, ```Benchmark```, ```Verification Project```|
| [Image gathering](https://github.com/Toloka/toloka-kit/tree/main/examples/image_gathering) <br/><br/> [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Toloka/toloka-kit/blob/main/examples/image_gathering/image_gathering.ipynb) | The goal for this project is to collect a dataset  of dogs' and cats' images. Performers will be asked to take a photo of their pet and specify its species. |```CV```,  ```Classification```, ```Collecting```, ```Dataset```|
| [Simplest Spatial Crowdsourcing](https://github.com/Toloka/toloka-kit/tree/main/examples/2.spatial_crowdsourcing/0.simplest_example) <br/><br/> [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Toloka/toloka-kit/blob/main/examples/2.spatial_crowdsourcing/0.simplest_example/spatial_crowdsourcing.ipynb) | In this example, we will collect pictures of the Moscow metro entrances. This example also can be reused for production tasks such as monitoring the state of objects, checking the presence of an organization or other physical object. |```Spatial Crowdsourcing```, ```Outdoor monitoring```, ```Collecting```|
| Blood cells classification | Available soon | ```CV```,  ```Classification```, ```Medicine```, ```Benchmark```|
# Need more examples?
If you have an example of data labeling using toloka-kit, do not hesitate to send us a [pool request](https://github.com/Toloka/toloka-kit/pulls). Ideally, a great example should contain the following aspects:
- Problem statement;
- How to set up a project;
- Where to get the data for the example;
- What to pay attention to when writing instructions;
- How to set up quality control;
- What is the final quality;
- Visualization of the obtained results;

You may also ask any question or ask for a new example using [issues](https://github.com/Toloka/toloka-kit/issues)
