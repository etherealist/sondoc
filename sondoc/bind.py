import os
from contextlib import contextmanager
from pathlib import Path
from subprocess import run
from tempfile import NamedTemporaryFile
from typing import List

css = """
html {
  line-height: 1.5;
  font-family: Georgia, serif;
  font-size: 20px;
  color: #1a1a1a;
  background-color: #fdfdf8;
}
body {
  margin: 0 auto;
  max-width: 36em;
  padding-left: 50px;
  padding-right: 50px;
  padding-top: 50px;
  padding-bottom: 50px;
  hyphens: auto;
  word-wrap: break-word;
  text-rendering: optimizeLegibility;
  font-kerning: normal;
}
@media (max-width: 600px) {
  body {
    font-size: 0.9em;
    padding: 1em;
  }
}
@media print {
  body {
    background-color: transparent;
    color: black;
    font-size: 10pt;
  }
  p, h2, h3 {
    orphans: 3;
    widows: 3;
  }
  h2, h3, h4 {
    page-break-after: avoid;
  }
  @page {
    size: A4;
    @bottom-center {
      font-size: 10pt;
      content: counter(page);
    }
  }
}
p {
  margin: 1em 0;
}
span.symbol {
  font-style: italic;
}
a {
  color: #164C73;
  text-decoration: none;
}
a:visited {
  color: #164C73;
  background-color: #ffffee;
}
img {
  max-width: 100%;
}
h1, h2, h3, h4, h5, h6 {
  margin-top: 1.4em;
}
h5, h6 {
  font-size: 1em;
  font-style: italic;
}
h6 {
  font-weight: normal;
}
ol, ul {
  padding-left: 1.7em;
  margin-top: 1em;
}
li > ol, li > ul {
  margin-top: 0;
}
blockquote {
  margin: 1em 0 1em 1.7em;
  padding-left: 1em;
  border-left: 2px solid #e6e6e6;
  color: #606060;
}
code {
  font-family: Menlo, Monaco, 'Lucida Console', Consolas, monospace;
  font-size: 85%;
  margin: 0;
}
pre {
  margin: 1em 0;
  overflow: auto;
}
pre code {
  padding: 0;
  overflow: visible;
}
.sourceCode {
 background-color: transparent;
 overflow: visible;
}
hr {
  background-color: #1a1a1a;
  border: none;
  height: 1px;
  margin: 1em 0;
}
table {
  margin: 1em 0;
  border-collapse: collapse;
  width: 100%;
  overflow-x: auto;
  display: block;
  font-variant-numeric: lining-nums tabular-nums;
}
table caption {
  margin-bottom: 0.75em;
}
tbody {
  margin-top: 0.5em;
  border-top: 1px solid #1a1a1a;
  border-bottom: 1px solid #1a1a1a;
}
th {
  border-top: 1px solid #1a1a1a;
  padding: 0.25em 0.5em 0.25em 0.5em;
}
td {
  padding: 0.125em 0.5em 0.25em 0.5em;
}
header {
  margin-bottom: 4em;
  text-align: center;
}
#TOC li {
  list-style: none;
}
#TOC a:not(:hover) {
  text-decoration: none;
}
"""


@contextmanager
def temp_css():
    with NamedTemporaryFile("w", encoding="UTF-8", suffix=".css") as temp:
        temp.write(css)
        temp.flush()
        yield temp.name


def bind(
    input: Path,
    output: Path,
    title: str = "No title",
    follow: bool = False,
) -> None:
    md_inputs: List[str] = []
    output_path = output.absolute()
    os.chdir(input)
    for root, _, files in os.walk(".", followlinks=follow):
        for file_ in files:
            if file_.endswith(".md"):
                md_inputs.append(os.path.join(root, file_))

    with temp_css() as temp:
        run(
            [
                "pandoc",
                "-s",
                "--toc",
                "--file-scope",
                "--self-contained",
                "--metadata",
                f"title={title}",
                "-c",
                temp,
                "-o",
                str(output_path),
            ]
            + sorted(md_inputs),
            check=True,
        )
    print(f"Bound: {output} {title}")
