EASE
====

.. image:: https://travis-ci.org/slaclab/ease.svg?branch=master
  :target: https://travis-ci.org/slaclab/ease
   
.. image:: https://codecov.io/gh/slaclab/ease/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/slaclab/ease

Authors: Nolan Brown, Victor Nieto, Ryan Dudschus, Daniel Douty

Epics remote alert system

See the `docs <https://slaclab.github.io/ease/>`_ for info.

Developing with Vagrant
-----------------------
Ease can be developed inside a virtual machine managed by the Vagrant utility. This offers the benefit of an isolated development environment. Vagrant can be automated to install all tools and dependencies for EASE using the vagrantfile.

Setup:
The vagrant getting started guide is an excellent way to get started.
https://www.vagrantup.com/intro/getting-started/index.html

To start the vagrant box:
`vagrant up`

The vagrant box will install everything you need and establish the ease-env.
