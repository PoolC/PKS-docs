#!/usr/bin/env python3

# Copyright 2025 Jesung Yang <y.jems.n@gmail.com>
# SPDX-License-Identifier: MIT

from PIL import Image
import os
import sys


def webpify(input_path: str, output_path: str) -> None:
    """
    Convert an image file to WebP format with quality compression.

    Args:
        input_path (str): Path to the input image file
        output_path (str): Path where the converted WebP file will be saved

    Raises:
        Exception: If the image conversion fails for any reason

    Note:
        The output WebP file is saved with quality=80 for optimal balance
        between file size and image quality.
    """
    try:
        with Image.open(input_path) as img:  # type: ignore [reportUnknownMemberType]
            img.save(output_path, format="WEBP", quality=80)  # type: ignore [reportUnknownMemberType]
            print(f"[INFO] Converted `{input_path}` to `{output_path}`")
    except Exception as e:
        print(f"[ERROR] Failed to convert `{input_path}` to WEBP: {e}", file=sys.stderr)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 webpify.py <input_path> <output_path>")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    if not os.path.exists(input_path):
        print(f"[ERROR] Input file `{input_path}` does not exist", file=sys.stderr)
        sys.exit(1)

    webpify(input_path, output_path)
