:py:mod:`nossis_docs.test.conftest`
===================================

.. py:module:: nossis_docs.test.conftest

.. autodoc2-docstring:: nossis_docs.test.conftest
   :allowtitles:

Module Contents
---------------

Functions
~~~~~~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`cloudfront <nossis_docs.test.conftest.cloudfront>`
     - .. autodoc2-docstring:: nossis_docs.test.conftest.cloudfront
          :summary:
   * - :py:obj:`distribution <nossis_docs.test.conftest.distribution>`
     - .. autodoc2-docstring:: nossis_docs.test.conftest.distribution
          :summary:

API
~~~

.. py:function:: cloudfront(_aws_credentials: None) -> mypy_boto3_cloudfront.CloudFrontClient
   :canonical: nossis_docs.test.conftest.cloudfront

   .. autodoc2-docstring:: nossis_docs.test.conftest.cloudfront

.. py:function:: distribution(faker: faker.Faker, cloudfront: mypy_boto3_cloudfront.CloudFrontClient) -> mypy_boto3_cloudfront.type_defs.CreateDistributionResultTypeDef
   :canonical: nossis_docs.test.conftest.distribution

   .. autodoc2-docstring:: nossis_docs.test.conftest.distribution
