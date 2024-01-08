"""
A hack to add autogenerate grpc code to the path
"""
import pathlib
import sys

sys.path.append(str(pathlib.Path(__file__).parent / "gen"))
