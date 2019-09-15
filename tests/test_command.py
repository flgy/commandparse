#!/usr/bin/env python3

from argparse import ArgumentParser
import argparse
from commandparse import Command, CommandTypeError
from mock import patch


class SampleCommand(Command):

	def opt_bool(self, kwargs):
		"""
		Test method that do something.

		Arguments:
			@verbose:bool
				The method will perform something and tell us about it
		"""
		assert "verbose" in kwargs
		assert isinstance(kwargs["verbose"], bool)
		assert kwargs["verbose"] is True or kwargs["verbose"] is False

	def opt_int(self, kwargs):
		"""
		Test method that do something.

		Arguments:
			@integer:int
				The method will perform something with `integer` if given
		"""
		assert "integer" in kwargs
		assert isinstance(kwargs["integer"], int) or kwargs["integer"] is None

	def opt_int_value(self, kwargs):
		"""
		Test method that do something.

		Arguments:
			@integer:int = 3
				The method will perform something with `integer` if given
		"""
		assert "integer" in kwargs
		assert isinstance(kwargs["integer"], int) or kwargs["integer"] is None

	def opt_int_values(self, kwargs):
		"""
		Test method that do something.

		Arguments:
			@integer:int = [0, 1, 1, 3, 5, 8]
				The method will perform something with `integer` if given
		"""
		assert "integer" in kwargs
		assert isinstance(kwargs["integer"], int) or kwargs["integer"] is None

	def opt_string(self, kwargs):
		"""
		Test method that do something.

		Arguments:
			@astring:string
				The method will perform something with `astring` if given
		"""
		assert "astring" in kwargs
		assert isinstance(kwargs["astring"], str) or kwargs["astring"] is None

	def opt_string_value(self, kwargs):
		"""
		Test method that do something.

		Arguments:
			@astring:string = 'foo'
				The method will perform something with `astring` if given
		"""
		assert "astring" in kwargs
		assert isinstance(kwargs["astring"], str) or kwargs["astring"] is None

	def opt_string_values(self, kwargs):
		"""
		Test method that do something.

		Arguments:
			@astring:string = ['foo', 'bar', 'qux']
				The method will perform something with `astring` if given
		"""
		assert "astring" in kwargs
		assert isinstance(kwargs["astring"], str) or kwargs["astring"] is None

	def opt_list(self, kwargs):
		"""
		Test method that do something.

		Arguments:
			@alist:list
				The method will perform something with `alist` if given
		"""
		assert "alist" in kwargs
		assert isinstance(kwargs["alist"], list) and (len(kwargs["alist"]) == 3 or len(kwargs["alist"]) == 0)

	def opt_list_values(self, kwargs):
		"""
		Test method that do something.

		Arguments:
			@alist:list = ['foo', 'bar', 'qux']
				The method will perform something with `alist` if given
		"""
		assert "alist" in kwargs
		assert isinstance(kwargs["alist"], list) and (len(kwargs["alist"]) == 3 or len(kwargs["alist"]) == 0)


	def pos_bool(self, kwargs):
		"""
		Test method that do something.

		Arguments:
			#verbose:bool
				The method will perform something and tell us about it
		"""
		assert "verbose" in kwargs
		assert isinstance(kwargs["verbose"], bool)
		assert kwargs["verbose"] is True or kwargs["verbose"] is False

	def pos_int(self, kwargs):
		"""
		Test method that do something.

		Arguments:
			#integer:int
				The method will perform something with `integer` if given
		"""
		assert "integer" in kwargs
		assert isinstance(kwargs["integer"], int) or kwargs["integer"] is None

	def pos_int_value(self, kwargs):
		"""
		Test method that do something.

		Arguments:
			#integer:int = 3
				The method will perform something with `integer` if given
		"""
		assert "integer" in kwargs
		assert isinstance(kwargs["integer"], int) or kwargs["integer"] is None

	def pos_int_values(self, kwargs):
		"""
		Test method that do something.

		Arguments:
			#integer:int = [0, 1, 1, 3, 5, 8]
				The method will perform something with `integer` if given
		"""
		assert "integer" in kwargs
		assert isinstance(kwargs["integer"], int) or kwargs["integer"] is None

	def pos_string(self, kwargs):
		"""
		Test method that do something.

		Arguments:
			#astring:string
				The method will perform something with `astring` if given
		"""
		assert "astring" in kwargs
		assert isinstance(kwargs["astring"], str) or kwargs["astring"] is None

	def pos_string_value(self, kwargs):
		"""
		Test method that do something.

		Arguments:
			#astring:string = 'foo'
				The method will perform something with `astring` if given
		"""
		assert "astring" in kwargs
		assert isinstance(kwargs["astring"], str) or kwargs["astring"] is None

	def pos_string_values(self, kwargs):
		"""
		Test method that do something.

		Arguments:
			#astring:string = ['foo', 'bar', 'qux']
				The method will perform something with `astring` if given
		"""
		assert "astring" in kwargs
		assert isinstance(kwargs["astring"], str) or kwargs["astring"] is None

	def pos_list(self, kwargs):
		"""
		Test method that do something.

		Arguments:
			#alist:list
				The method will perform something with `alist` if given
		"""
		assert "alist" in kwargs
		assert (isinstance(kwargs["alist"], list) and len(kwargs["alist"]) == 3) or kwargs["alist"] is None

	def pos_list_values(self, kwargs):
		"""
		Test method that do something.

		Arguments:
			#alist:list = ['foo', 'bar', 'qux']
				The method will perform something with `alist` if given
		"""
		assert "alist" in kwargs
		assert (isinstance(kwargs["alist"], list) and len(kwargs["alist"]) == 2) or kwargs["alist"] is None

	def multiple_opts_with_same_prefix(self, kwargs):
		"""
		Test method that do something.
		Arguments:
			@verbose:bool
				The method will perform something and be verbose about it
			@value:int = 2
				The method will perform something with `value` if given
		"""
		assert "verbose" in kwargs
		assert "value" in kwargs
		assert isinstance(kwargs["verbose"], bool) and isinstance(kwargs["value"], int)

class TestCommand():

	def test_bool_option_set(self):
		parser = ArgumentParser()
		sub = parser.add_subparsers()

		SampleCommand.set_subparser_for("bool", "opt_bool", sub)
		args = parser.parse_known_args(["bool", "-v"])[0]
		cmd = SampleCommand()
		cmd.opt_bool(vars(args))

	def test_bool_option_not_set(self):
		parser = ArgumentParser()
		sub = parser.add_subparsers()

		SampleCommand.set_subparser_for("bool", "opt_bool", sub)
		args = parser.parse_known_args(["bool"])[0]
		cmd = SampleCommand()
		cmd.opt_bool(vars(args))

	def test_int_option_incorrectly_set(self):
		parser = ArgumentParser()
		sub = parser.add_subparsers()

		SampleCommand.set_subparser_for("int", "opt_int", sub)
		with patch("argparse.ArgumentParser.exit") as argparse_exit:
			try:
				args = parser.parse_known_args(["int", "-i", "asd"])[0]
			except TypeError:
				pass

	def test_int_option_set(self):
		parser = ArgumentParser()
		sub = parser.add_subparsers()

		SampleCommand.set_subparser_for("int", "opt_int", sub)
		args = parser.parse_known_args(["int", "-i", "2"])[0]
		cmd = SampleCommand()
		cmd.opt_int(vars(args))

	def test_int_option_not_set(self):
		parser = ArgumentParser()
		sub = parser.add_subparsers()

		SampleCommand.set_subparser_for("int", "opt_int", sub)
		args = parser.parse_known_args(["int"])[0]
		cmd = SampleCommand()
		cmd.opt_int(vars(args))

	def test_int_option_value(self):
		parser = ArgumentParser()
		sub = parser.add_subparsers()

		SampleCommand.set_subparser_for("int_value", "opt_int_value", sub)
		args = parser.parse_known_args(["int_value", "-i", "3"])[0]
		cmd = SampleCommand()
		cmd.opt_int_value(vars(args))

	def test_int_option_values(self):
		parser = ArgumentParser()
		sub = parser.add_subparsers()

		SampleCommand.set_subparser_for("int_values", "opt_int_values", sub)
		args = parser.parse_known_args(["int_values", "-i", "3"])[0]
		cmd = SampleCommand()
		cmd.opt_int_values(vars(args))

	def test_string_option_set(self):
		parser = ArgumentParser()
		sub = parser.add_subparsers()

		SampleCommand.set_subparser_for("string", "opt_string", sub)
		args = parser.parse_known_args(["string", "-a", "test"])[0]
		cmd = SampleCommand()
		cmd.opt_string(vars(args))

	def test_string_option_not_set(self):
		parser = ArgumentParser()
		sub = parser.add_subparsers()

		SampleCommand.set_subparser_for("string", "opt_string", sub)
		args = parser.parse_known_args(["string"])[0]
		cmd = SampleCommand()
		cmd.opt_string(vars(args))

	def test_string_option_value(self):
		parser = ArgumentParser()
		sub = parser.add_subparsers()

		SampleCommand.set_subparser_for("string_value", "opt_string_value", sub)
		args = parser.parse_known_args(["string_value", "-a", "foo"])[0]
		cmd = SampleCommand()
		cmd.opt_string_value(vars(args))

	def test_string_option_values(self):
		parser = ArgumentParser()
		sub = parser.add_subparsers()

		SampleCommand.set_subparser_for("string_values", "opt_string_values", sub)
		args = parser.parse_known_args(["string_values", "-a", "qux"])[0]
		cmd = SampleCommand()
		cmd.opt_string_values(vars(args))


	def test_list_option_set(self):
		parser = ArgumentParser()
		sub = parser.add_subparsers()

		SampleCommand.set_subparser_for("list", "opt_list", sub)
		args = parser.parse_known_args(["list", "-a", "foo", "bar", "qux"])[0]
		cmd = SampleCommand()
		cmd.opt_list(vars(args))

	def test_list_option_not_set(self):
		parser = ArgumentParser()
		sub = parser.add_subparsers()

		SampleCommand.set_subparser_for("list", "opt_list", sub)
		args = parser.parse_known_args(["list"])[0]
		cmd = SampleCommand()
		cmd.opt_list(vars(args))

	def test_list_option_values(self):
		parser = ArgumentParser()
		sub = parser.add_subparsers()

		SampleCommand.set_subparser_for("list_values", "opt_list_values", sub)
		args = parser.parse_known_args(["list_values", "-a", "foo", "bar", "qux"])[0]
		cmd = SampleCommand()
		cmd.opt_list_values(vars(args))

	def test_bool_position_set(self):
		parser = ArgumentParser()
		sub = parser.add_subparsers()

		try:
			SampleCommand.set_subparser_for("bool", "pos_bool", sub)
		except CommandTypeError:
			pass

	def test_bool_position_not_set(self):
		parser = ArgumentParser()
		sub = parser.add_subparsers()

		try:
			SampleCommand.set_subparser_for("bool", "pos_bool", sub)
		except CommandTypeError:
			pass

	def test_int_position_set(self):
		parser = ArgumentParser()
		sub = parser.add_subparsers()

		SampleCommand.set_subparser_for("int", "pos_int", sub)
		args = parser.parse_known_args(["int", "2"])[0]
		cmd = SampleCommand()
		cmd.pos_int(vars(args))

	def test_int_position_not_set(self):
		parser = ArgumentParser()
		sub = parser.add_subparsers()

		SampleCommand.set_subparser_for("int", "pos_int", sub)
		with patch("argparse.ArgumentParser.exit") as argparse_exit:
			args = parser.parse_known_args(["int"])[0]
			cmd = SampleCommand()
			cmd.pos_int(vars(args))

	def test_int_position_value(self):
		parser = ArgumentParser()
		sub = parser.add_subparsers()

		SampleCommand.set_subparser_for("int_value", "opt_int_value", sub)
		args = parser.parse_known_args(["int_value", "3"])[0]
		cmd = SampleCommand()
		cmd.opt_int_value(vars(args))

	def test_int_position_values(self):
		parser = ArgumentParser()
		sub = parser.add_subparsers()

		SampleCommand.set_subparser_for("int_values", "opt_int_values", sub)
		args = parser.parse_known_args(["int_values", "3"])[0]
		cmd = SampleCommand()
		cmd.opt_int_values(vars(args))

	def test_string_position_set(self):
		parser = ArgumentParser()
		sub = parser.add_subparsers()

		SampleCommand.set_subparser_for("string", "pos_string", sub)
		args = parser.parse_known_args(["string", "test"])[0]
		cmd = SampleCommand()
		cmd.pos_string(vars(args))

	def test_string_position_not_set(self):
		parser = ArgumentParser()
		sub = parser.add_subparsers()

		SampleCommand.set_subparser_for("string", "pos_string", sub)
		with patch("argparse.ArgumentParser.exit") as argparse_exit:
			args = parser.parse_known_args(["string"])[0]
			cmd = SampleCommand()
			cmd.pos_string(vars(args))

	def test_string_position_value(self):
		parser = ArgumentParser()
		sub = parser.add_subparsers()

		SampleCommand.set_subparser_for("string_value", "pos_string_value", sub)
		args = parser.parse_known_args(["string_value", "foo"])[0]
		cmd = SampleCommand()
		cmd.pos_string_value(vars(args))

	def test_string_position_values(self):
		parser = ArgumentParser()
		sub = parser.add_subparsers()

		SampleCommand.set_subparser_for("string_values", "pos_string_values", sub)
		args = parser.parse_known_args(["string_values", "qux"])[0]
		cmd = SampleCommand()
		cmd.pos_string_values(vars(args))

	def test_list_option_set(self):
		parser = ArgumentParser()
		sub = parser.add_subparsers()

		SampleCommand.set_subparser_for("list", "pos_list", sub)
		args = parser.parse_known_args(["list", "foo", "bar", "qux"])[0]
		cmd = SampleCommand()
		cmd.pos_list(vars(args))

	def test_list_position_set(self):
		parser = ArgumentParser()
		sub = parser.add_subparsers()

		SampleCommand.set_subparser_for("list", "pos_list", sub)
		args = parser.parse_known_args(["list", "foo", "bar", "qux"])[0]
		cmd = SampleCommand()
		cmd.pos_list(vars(args))

	def test_list_position_not_set(self):
		parser = ArgumentParser()
		sub = parser.add_subparsers()

		SampleCommand.set_subparser_for("list", "pos_list", sub)
		with patch("argparse.ArgumentParser.exit") as argparse_exit:
			args = parser.parse_known_args(["list"])[0]
			cmd = SampleCommand()
			cmd.pos_list(vars(args))

	def test_list_position_values(self):
		parser = ArgumentParser()
		sub = parser.add_subparsers()

		SampleCommand.set_subparser_for("list_values", "pos_list_values", sub)
		args = parser.parse_known_args(["list_values", "bar", "qux"])[0]
		cmd = SampleCommand()
		cmd.pos_list_values(vars(args))

	def test_retrieve_default_val_for_arg(self):
		cmd = SampleCommand()
		assert cmd.retrieve_default_val_for_arg("pos_list", "alist") is None
		assert cmd.retrieve_default_val_for_arg("pos_list_values", "alist") == ["foo", "bar", "qux"]

	def test_multiple_opts_with_same_prefix(self):
		parser = ArgumentParser()
		sub = parser.add_subparsers()

		SampleCommand.set_subparser_for("multiple_opts_with_same_prefix", "multiple_opts_with_same_prefix", sub)
		args = parser.parse_known_args(["multiple_opts_with_same_prefix", "-v", "--value", "2"])[0]
		cmd = SampleCommand()
		cmd.multiple_opts_with_same_prefix(vars(args))
