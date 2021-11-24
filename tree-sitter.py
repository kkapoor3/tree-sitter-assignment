from tree_sitter import Language, Parser
from autoscraper import AutoScraper
import requests
from git import Repo
from pathlib import Path

Language.build_library(
  
  'build/my-languages.so',

  [
    './tree-sitter-go',
    './tree-sitter-javascript',
    './tree-sitter-python',
    './tree-sitter-ruby'
  ]
)

repo = input("Enter GitHub repo link")

lang = int(input("Enter language name \n 1.) Python(.py) \n 2.) JavaScript(.js) \n 3.) Ruby(.rb) \n 4.) GO(.go)"))

if lang not in [1,2,3,4]:
  print("Please enter a valid output")

if lang == 1:
  LANG = 'python'
elif lang == 2:
  LANG = 'javascript'
elif lang == 3:
  LANG = 'ruby'
elif lang == 4:
  LANG = 'go'

LANGUAGE = Language('build/my-languages.so', LANG)
parser = Parser()
parser.set_language(LANGUAGE)

tree = parser.parse(bytes("""
def foo():
    if bar:
        baz()
""", "utf8"))

# root_node = tree.root_node

# print(root_node)
# print(root_node.children)
# print(root_node.children[0])

query = LANGUAGE.query("""
(function_definition
  name: (identifier) @function.def)

(call
  function: (identifier) @function.call)
""")

captures = query.captures(tree.root_node)

for capture in captures:
  print(capture[1])


url = 'https://github.com/alirezamika/autoscraper'

# wanted_list = [""]

# scraper = AutoScraper()
# result = scraper.build(url, wanted_list)
# print(result)

# Repo.clone_from(url, './repo')

for path in Path('./repo').rglob('*.py'):
  print(path.name)

  f = open(path, "r")
  g = open(path, "r")

  # print(f.read())

  data = g.readlines()
  print(data)

  tree = parser.parse(bytes(f.read(), "utf8"))

  root_node = tree.root_node
  
  # print("name", root_node.children[0].child_by_field_name('name'))
  print(root_node.children)


  # print(root_node.sexp(), "\n\n\n\n\n\n\n\n")

  query = LANGUAGE.query("""
  (function_definition
    name: (identifier) @function.def)

  (call
    function: (identifier) @function.call)""")

  captures = query.captures(root_node)

  for capture in captures:
    print(capture)
    print(capture[0].start_point)
    print(capture[0].end_point)
    i = capture[0].start_point[0] + 1
    j = capture[0].start_point[1] - 1
    print(data[i])
    print(data[i][j])

    idf = ""

    for k in data[i]:
      if k == "(" or k == "=" or k == " ":
        if idf!= "":
          break
        else:
          continue

      else:
        idf += k
        
      print(idf)

      

    # print(root_node.sexp()[capture[0].start_point[0]][capture[0].start_point[1]])

  # for child in root_node.children:
  #   print(child.type)

  