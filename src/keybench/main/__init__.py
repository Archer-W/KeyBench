# -*- encoding: utf-8 -*-

from keybench.main import component
from keybench.main import core
from keybench.main import exception
from keybench.main import factory
from keybench.main import language_support
from keybench.main import model
from keybench.main import nlp_tool

def launch(run_configurations, run_tools, run_resources):
  benchmark = core.KBBenchmark.singleton()

  benchmark.run_configurations = run_configurations
  benchmark.run_tools = run_tools
  benchmark.run_resources = run_resources

  benchmark.start()

