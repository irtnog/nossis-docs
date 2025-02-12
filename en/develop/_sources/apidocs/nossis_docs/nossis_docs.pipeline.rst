:py:mod:`nossis_docs.pipeline`
==============================

.. py:module:: nossis_docs.pipeline

.. autodoc2-docstring:: nossis_docs.pipeline
   :allowtitles:

Module Contents
---------------

Functions
~~~~~~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`invalidate_distribution <nossis_docs.pipeline.invalidate_distribution>`
     - .. autodoc2-docstring:: nossis_docs.pipeline.invalidate_distribution
          :summary:

Data
~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`logger <nossis_docs.pipeline.logger>`
     - .. autodoc2-docstring:: nossis_docs.pipeline.logger
          :summary:
   * - :py:obj:`cloudfront <nossis_docs.pipeline.cloudfront>`
     - .. autodoc2-docstring:: nossis_docs.pipeline.cloudfront
          :summary:
   * - :py:obj:`codepipeline <nossis_docs.pipeline.codepipeline>`
     - .. autodoc2-docstring:: nossis_docs.pipeline.codepipeline
          :summary:

API
~~~

.. py:data:: logger
   :canonical: nossis_docs.pipeline.logger
   :value: 'getLogger(...)'

   .. autodoc2-docstring:: nossis_docs.pipeline.logger

.. py:data:: cloudfront
   :canonical: nossis_docs.pipeline.cloudfront
   :type: mypy_boto3_cloudfront.CloudFrontClient
   :value: 'client(...)'

   .. autodoc2-docstring:: nossis_docs.pipeline.cloudfront

.. py:data:: codepipeline
   :canonical: nossis_docs.pipeline.codepipeline
   :type: mypy_boto3_codepipeline.CodePipelineClient
   :value: 'client(...)'

   .. autodoc2-docstring:: nossis_docs.pipeline.codepipeline

.. py:function:: invalidate_distribution(event: aws_lambda_powertools.utilities.data_classes.CodePipelineJobEvent, context: aws_lambda_powertools.utilities.typing.LambdaContext) -> None
   :canonical: nossis_docs.pipeline.invalidate_distribution

   .. autodoc2-docstring:: nossis_docs.pipeline.invalidate_distribution
