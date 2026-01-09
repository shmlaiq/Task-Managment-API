#!/usr/bin/env python3
"""
Generate test file stubs for Python modules.

Usage:
    python generate_tests.py <source_file> [output_dir]

Examples:
    python generate_tests.py src/utils.py
    python generate_tests.py src/api/handlers.py tests/
"""

import ast
import sys
from pathlib import Path


def extract_functions_and_classes(source_code: str) -> dict:
    """Parse Python source and extract function/class definitions."""
    tree = ast.parse(source_code)

    result = {
        "functions": [],
        "classes": [],
    }

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            # Skip private functions (single underscore) and dunder methods
            if not node.name.startswith("_"):
                params = [arg.arg for arg in node.args.args if arg.arg != "self"]
                result["functions"].append({
                    "name": node.name,
                    "params": params,
                    "is_async": False,
                })
        elif isinstance(node, ast.AsyncFunctionDef):
            if not node.name.startswith("_"):
                params = [arg.arg for arg in node.args.args if arg.arg != "self"]
                result["functions"].append({
                    "name": node.name,
                    "params": params,
                    "is_async": True,
                })
        elif isinstance(node, ast.ClassDef):
            if not node.name.startswith("_"):
                methods = []
                for item in node.body:
                    if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        if not item.name.startswith("_") or item.name == "__init__":
                            methods.append(item.name)
                result["classes"].append({
                    "name": node.name,
                    "methods": methods,
                })

    return result


def generate_test_code(module_name: str, definitions: dict) -> str:
    """Generate pytest test file content."""
    lines = [
        '"""',
        f"Tests for {module_name}",
        '"""',
        "",
        "import pytest",
        f"from {module_name.replace('/', '.').replace('.py', '')} import (",
    ]

    # Import items
    items_to_import = []
    for func in definitions["functions"]:
        items_to_import.append(f"    {func['name']},")
    for cls in definitions["classes"]:
        items_to_import.append(f"    {cls['name']},")

    if items_to_import:
        lines.extend(items_to_import)
        lines.append(")")
    else:
        lines[-1] = f"# from {module_name.replace('/', '.').replace('.py', '')} import ..."

    lines.append("")
    lines.append("")

    # Generate function tests
    for func in definitions["functions"]:
        if func["is_async"]:
            lines.append("@pytest.mark.asyncio")
            lines.append(f"async def test_{func['name']}():")
        else:
            lines.append(f"def test_{func['name']}():")

        lines.append(f'    """Test {func["name"]} function."""')

        if func["params"]:
            params_str = ", ".join(f"{p}=None" for p in func["params"])
            if func["is_async"]:
                lines.append(f"    result = await {func['name']}({params_str})")
            else:
                lines.append(f"    result = {func['name']}({params_str})")
        else:
            if func["is_async"]:
                lines.append(f"    result = await {func['name']}()")
            else:
                lines.append(f"    result = {func['name']}()")

        lines.append("    assert result is not None  # TODO: Add proper assertions")
        lines.append("")
        lines.append("")

    # Generate class tests
    for cls in definitions["classes"]:
        lines.append(f"class Test{cls['name']}:")
        lines.append(f'    """Tests for {cls["name"]} class."""')
        lines.append("")
        lines.append("    @pytest.fixture")
        lines.append(f"    def {cls['name'].lower()}(self):")
        lines.append(f'        """Create {cls["name"]} instance for testing."""')
        lines.append(f"        return {cls['name']}()  # TODO: Add constructor args")
        lines.append("")

        for method in cls["methods"]:
            if method == "__init__":
                lines.append("    def test_initialization(self):")
                lines.append(f'        """Test {cls["name"]} initialization."""')
                lines.append(f"        obj = {cls['name']}()  # TODO: Add constructor args")
                lines.append("        assert obj is not None")
            else:
                lines.append(f"    def test_{method}(self, {cls['name'].lower()}):")
                lines.append(f'        """Test {method} method."""')
                lines.append(f"        result = {cls['name'].lower()}.{method}()")
                lines.append("        assert result is not None  # TODO: Add proper assertions")
            lines.append("")
        lines.append("")

    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_tests.py <source_file> [output_dir]")
        print("Example: python generate_tests.py src/utils.py tests/")
        sys.exit(1)

    source_file = Path(sys.argv[1])
    output_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("tests")

    if not source_file.exists():
        print(f"Error: Source file '{source_file}' not found")
        sys.exit(1)

    # Read source file
    source_code = source_file.read_text()

    # Extract definitions
    definitions = extract_functions_and_classes(source_code)

    if not definitions["functions"] and not definitions["classes"]:
        print(f"No public functions or classes found in {source_file}")
        sys.exit(0)

    # Generate test code
    test_code = generate_test_code(str(source_file), definitions)

    # Create output directory if needed
    output_dir.mkdir(parents=True, exist_ok=True)

    # Write test file
    test_filename = f"test_{source_file.stem}.py"
    output_file = output_dir / test_filename

    output_file.write_text(test_code)
    print(f"Generated: {output_file}")
    print(f"  - {len(definitions['functions'])} function(s)")
    print(f"  - {len(definitions['classes'])} class(es)")


if __name__ == "__main__":
    main()
