BLOCK_TYPE = [
 "paragraph",
 "heading",
 "code",
 "quote",
 "unordered_list",
 "ordered_list"
]

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"

def markdown_to_blocks(markdown):
 return list(filter(lambda x: x != "", markdown.split("\n\n")))
 
def block_to_block_type(block):
 def is__(doc, fun):
  doc = doc.split("\n")
  for line in doc:
   if not fun(line):
    return False
  
  return True   
 
 if block.split()[0] in "######":
  return block_type_heading
 elif len(block) >= 6 and block[:3] == "```" and block[-3:] == "```":
  return block_type_code
  
 elif is__(block, lambda line: line[0] == ">"):
  return block_type_quote

 elif is__(block, lambda line: line[:2] in ["- ", "* "]):
  return block_type_unordered_list

 elif [line[:3] for line in block.split("\n")] == [f".{i} " for i in range(len(block.split("\n")))]:
  return block_type_ordered_list

 else:
  return block_type_paragraph