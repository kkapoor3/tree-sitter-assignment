from tree_sitter import Language, Parser
from git import Repo
from pathlib import Path
import re
import shutil

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

output1 = input("Enter file path output 1")
output2 = input("Enter file path output 2")

o1 = open(output1, "w")
o1.write("")

o2 = open(output2, "w")
o2.write("")

if lang not in [1,2,3,4]:
  print("Please enter a valid output")

if lang == 1:
  LANG = 'python'
  EXTENSION = '*.py'
elif lang == 2:
  LANG = 'javascript'
  EXTENSION = '*.js'
elif lang == 3:
  LANG = 'ruby'
  EXTENSION = '*.rb'
elif lang == 4:
  LANG = 'go'
  EXTENSION = '*.go'

LANGUAGE = Language('build/my-languages.so', LANG)
parser = Parser()
parser.set_language(LANGUAGE)

shutil.rmtree('./repo', ignore_errors=True)

Repo.clone_from(repo, './repo')

for path in Path('./repo').rglob(EXTENSION):

  f = open(path, "r")
  g = open(path, "r")

  data = g.readlines()

  tree = parser.parse(bytes(f.read(), "utf8"))

  root_node = tree.root_node

  query = LANGUAGE.query("""
  (function_definition
    name: (identifier) @function.def)

  (call
    function: (identifier) @function.call)""")

  captures = query.captures(root_node)

  o1 = open(output1, "a")
  o1.write(path.name)
  o1.write("\n\n")

  o2 = open(output2, "a")
  o2.write(path.name)
  o2.write("\n\n")

  for capture in captures:
    i = capture[0].start_point[0] + 1
    j = capture[0].start_point[1] - 1

    if i < len(data):

      idf = ""

      for k in data[i]:
        if k == "(" or k == "=" or k == " ":
          if idf!= "":
            break
          else:
            continue

        else:
          idf += k


      write_data = " identifier_name - " + idf + "\n start_point - " + str(capture[0].start_point) + "\n end_point - " + str(capture[0].end_point) + "\n\n"

      o1.write(write_data)

      consecutive_uppercase = re.findall("([A-Z]){2}", idf)
      consecutive_underscores = re.findall("__", idf)
      uppercase = re.findall("([A-Z])", idf)
      leading_underscores = re.findall("^_", idf)
      trailing_underscores = re.findall("_$", idf)
      idf_length = len(idf) 

      acceptable_idf = ['c','d','e','g','i','in','inOut','j','k','m','n','o','out','t','x','y','z']

      if idf_length < 8 and idf not in acceptable_idf:
        write_data = " identifier_name - " + idf + "\n start_point - " + str(capture[0].start_point) + "\n end_point - " + str(capture[0].end_point) + "\n Rule Violated - Short Identifier Name" + "\n\n"
        o2.write(write_data)
        
      elif idf_length > 16:
        write_data = " identifier_name - " + idf + "\n start_point - " + str(capture[0].start_point) + "\n end_point - " + str(capture[0].end_point) + "\n Rule Violated - Long Identifier Name" + "\n\n"
        o2.write(write_data)

      elif consecutive_underscores:
        write_data = " identifier_name - " + idf + "\n start_point - " + str(capture[0].start_point) + "\n end_point - " + str(capture[0].end_point) + "\n Rule Violated - Consecutive Underscores" + "\n\n"
        o2.write(write_data)

      elif consecutive_uppercase:
        write_data = " identifier_name - " + idf + "\n start_point - " + str(capture[0].start_point) + "\n end_point - " + str(capture[0].end_point) + "\n Rule Violated - Capitalization Anomaly" + "\n\n"
        o2.write(write_data)

      if len(uppercase) > 4:
        write_data = " identifier_name - " + idf + "\n start_point - " + str(capture[0].start_point) + "\n end_point - " + str(capture[0].end_point) + "\n Rule Violated - Excessive Words / Number of Words" + "\n\n"
        o2.write(write_data)

      if leading_underscores or trailing_underscores:
        write_data = " identifier_name - " + idf + "\n start_point - " + str(capture[0].start_point) + "\n end_point - " + str(capture[0].end_point) + "\n Rule Violated - External Underscores" + "\n\n"
        o2.write(write_data)


  