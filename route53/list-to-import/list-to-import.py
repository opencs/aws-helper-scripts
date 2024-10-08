# Copyright 2024 Open Communications Security LTDA.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#    1. Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#
#    2. Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#
#    3. Neither the name of the copyright holder nor the names of its
#       contributors may be used to endorse or promote products derived from
#       this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS “AS IS”
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
import argparse
import json
from pathlib import Path
import sys

IGNORE_EXISTING = {'SOA', 'NS'}
"""
Types of entries that must be filtered out.
"""


def convert(src: Path, dst: Path):
    with open(src, 'r') as inp:
        src = json.load(inp)

    ret = []
    for entry in src['ResourceRecordSets']:
        if entry["Type"] not in IGNORE_EXISTING:
            new_entry = {
                "Action": "CREATE",
                "ResourceRecordSet": {
                    'ResourceRecords': entry['ResourceRecords'],
                    "Type": entry['Type'],
                    "Name": entry['Name'],
                    "TTL": entry['TTL'],
                },
            }
            ret.append(new_entry)
    ret = {
        "Comment": "import file generated by list-to-import.py",
        "Changes": ret
    }
    with open(dst, 'w') as outp:
        json.dump(ret, outp, indent=4)


def main():
    parser = argparse.ArgumentParser(
        description="""
list-to-import.py is a small script that converts the results of the aws route53
command list-resource-record-sets into the input required by the command 
change-resource-record-sets as described in the article 
https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/hosted-zones-migrating.html#hosted-zones-migrating-create-file.
""",
        epilog='This script was released under the terms of '
    )
    parser.add_argument(
        '-i', '--input',
        metavar='input_file.json',
        required=True,
        help='The listing generated by `aws route53 list-resource-record-sets`.',
    )
    parser.add_argument(
        '-o', '--output',
        metavar='change_batch.json',
        required=True,
        help='The change-batch required by by `aws route53 change-resource-record-sets`.',
    )
    args = parser.parse_args()
    src = Path(args.input)
    dst = Path(args.output)
    if not src.is_file():
        print(f'{src} does not exist.', file=sys.stderr)
        sys.exit(1)
    convert(src, dst)


if __name__ == '__main__':
    main()
