import os
import subprocess
import sys
import tempfile
from typing import Dict

from app.tool.base import BaseTool


class PythonExecute(BaseTool):
    """A tool for executing Python code with timeout and safety restrictions."""

    name: str = "python_execute"
    description: str = "Executes Python code string. Note: Only print outputs are visible, function return values are not captured. Use print statements to see results."
    parameters: dict = {
        "type": "object",
        "properties": {
            "code": {
                "type": "string",
                "description": "The Python code to execute.",
            },
        },
        "required": ["code"],
    }

    async def execute(
        self,
        code: str,
        timeout: int = 5,
    ) -> Dict:
        """
        Executes the provided Python code with a timeout.
        Uses /usr/local/bin/python3 (Docker image) instead of host Python.
        """
        # Use Python from Docker image, not host
        python_path = "/usr/local/bin/python3"
        if not os.path.exists(python_path):
            python_path = sys.executable

        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            temp_path = f.name

        try:
            proc = subprocess.Popen(
                [python_path, temp_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
            )
            try:
                stdout, _ = proc.communicate(timeout=timeout)
                return {
                    "observation": stdout,
                    "success": proc.returncode == 0,
                }
            except subprocess.TimeoutExpired:
                proc.kill()
                proc.wait()
                return {
                    "observation": f"Execution timeout after {timeout} seconds",
                    "success": False,
                }
        except Exception as e:
            return {
                "observation": str(e),
                "success": False,
            }
        finally:
            try:
                os.unlink(temp_path)
            except OSError:
                pass
