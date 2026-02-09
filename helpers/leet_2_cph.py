#!/usr/bin/env python3
"""
Create a CPH style list from an input list of items.
For a leetcode style input like:
[1, 2, 3, 4]
[[1, 2], [3, 4]]

CPH style output would be:
4 -> number of items in the list
1 -> first item in the list
2 -> second item in the list
3 -> third item in the list
4 -> fourth item in the list

2 -> number of items in the outer list
1 2 -> first inner list
3 4 -> second inner list

this helper is useful for converting leetcode style inputs to CPH style inputs
this is to help you get the test cases for the CPH extension in the correct format
"""

from __future__ import annotations

import ast
import sys
from typing import Iterable, List


def _normalize_input(raw: str) -> str:
	normalized = raw.strip()
	if not normalized:
		return normalized
	normalized = normalized.replace("null", "None")
	normalized = normalized.replace("true", "True")
	normalized = normalized.replace("false", "False")
	return normalized


def _quote_if_needed(token: str) -> str:
	lowered = token.lower()
	if lowered in {"true", "false", "null", "none"}:
		return token

	numeric = token.replace("_", "")
	if numeric.lstrip("-").replace(".", "", 1).isdigit():
		return token

	escaped = token.replace('"', "\\\"")
	return f'"{escaped}"'


def _quote_bare_tokens(raw: str) -> str:
	output: List[str] = []
	token: List[str] = []
	in_quote: str | None = None
	escape = False

	for ch in raw:
		if in_quote:
			output.append(ch)
			if escape:
				escape = False
			elif ch == "\\":
				escape = True
			elif ch == in_quote:
				in_quote = None
			continue

		if ch in {"\"", "'"}:
			output.append(ch)
			in_quote = ch
			continue

		if ch in {"[", "]", ","}:
			current = "".join(token).strip()
			if current:
				output.append(_quote_if_needed(current))
			token = []
			output.append(ch)
			continue

		token.append(ch)

	current = "".join(token).strip()
	if current:
		output.append(_quote_if_needed(current))

	return "".join(output)


def _format_scalar(value: object) -> str:
	if value is None:
		return "null"
	if isinstance(value, bool):
		return "true" if value else "false"
	return str(value)


def _is_sequence(value: object) -> bool:
	return isinstance(value, (list, tuple))


def _format_1d(values: Iterable[object]) -> List[str]:
	values_list = list(values)
	lines = [str(len(values_list))]
	lines.extend(_format_scalar(item) for item in values_list)
	return lines


def _format_2d(values: Iterable[Iterable[object]]) -> List[str]:
	outer = list(values)
	lines = [str(len(outer))]
	for row in outer:
		row_items = list(row)
		lines.append(" ".join(_format_scalar(item) for item in row_items))
	return lines


def leet_to_cph(value: object) -> List[str]:
	if not _is_sequence(value):
		raise ValueError("Input must be a list or list of lists.")

	items = list(value)
	if not items:
		return ["0"]

	is_all_sequences = all(_is_sequence(item) for item in items)
	is_any_sequences = any(_is_sequence(item) for item in items)

	if is_all_sequences:
		return _format_2d(items)
	if is_any_sequences:
		raise ValueError("Mixed list types: expected all scalars or all lists.")

	return _format_1d(items)


def _read_input(argv: List[str]) -> str:
	if len(argv) > 1:
		return " ".join(argv[1:])
	return sys.stdin.read()


def main() -> None:
	if any(arg in {"-h", "--help"} for arg in sys.argv[1:]):
		print("Usage: python helpers/leet_2_cph.py '[1, 2, 3]'", file=sys.stderr)
		print("   or: echo '[ [1,2], [3,4] ]' | python helpers/leet_2_cph.py", file=sys.stderr)
		raise SystemExit(0)

	raw = _read_input(sys.argv)
	normalized = _normalize_input(raw)

	if not normalized:
		print("No input provided.", file=sys.stderr)
		raise SystemExit(1)

	try:
		parsed = ast.literal_eval(normalized)
	except (ValueError, SyntaxError):
		try:
			sanitized = _quote_bare_tokens(normalized)
			parsed = ast.literal_eval(sanitized)
		except (ValueError, SyntaxError) as exc:
			print(f"Invalid input: {exc}", file=sys.stderr)
			raise SystemExit(1)

	try:
		lines = leet_to_cph(parsed)
	except ValueError as exc:
		print(f"Invalid input: {exc}", file=sys.stderr)
		raise SystemExit(1)

	sys.stdout.write("\n".join(lines))


if __name__ == "__main__":
	main()
