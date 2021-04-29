# Toloka-kit usage examples
## _Data collection, markup, aggregation, and other applications_ 

Why it may be usefull:
- Easily reuse projects by just copying and pasting code. No need to configure parameters in the interface over and over again.   
- Train your ML models and run your data labeling projects in the same environment. 
- Take advantage of open-source code that anyone can use and contribute to. 

## Table of content

| Example | Abstract | Key words |
| ------ | ------ | ------ |
| [Image segmentation/detection](https://github.com/Toloka/toloka-kit/tree/main/examples/image_segmentation) | Example of solving the classic problem of annotating images for training segmentation algorithms. In real-world tasks, annotation is usually done with a polygon. We chose to use a rectangular outline to simplify the task so that we can reduce costs and speed things up. |```CV```, ```Segmentation```,  ```Detection```, ```Bounding boxes```, ```Street```, ```Traffic sign```|
| [Questing answering on SQuAD](https://github.com/Toloka/toloka-kit/tree/main/examples/SQUAD2.0) | Solving the problem of question answering on SQUAD2.0 dataset. Collects and validates answers for questions by human performers. One of the most popular tasks in natural language processing. | ```NLP```, ```Questing Answering```, ```Texts```, ```Benchmark```|
| [Image gathering](https://github.com/Toloka/toloka-kit/tree/main/examples/image_gathering) | The goal for this project is to collect a dataset  of dogs' and cats' images. Performers will be asked to take a photo of their pet and specify its species. |```CV```,  ```Classification```, ```Collecting```, ```Dataset```|
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
