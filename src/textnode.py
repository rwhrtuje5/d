ACCEPTABLE_TEXT_TYPE = ["text", "bold", "italic", "code", "link", "image"]
text_type_text, text_type_bold, text_type_italic, text_type_code, text_type_link, text_type_image = ACCEPTABLE_TEXT_TYPE
import re

class TextNode:
 def __init__(self, text, text_type, url = None):
  self.text = text
  self.text_type = text_type
  self.url = url
 def __eq__(self, otherTextNode):
  if self.text != otherTextNode.text: 
   return False
  if self.text_type != otherTextNode.text_type:
   return False
  if self.url != otherTextNode.url:
   return False
  return True
 def __repr__(self):
  return f"TextNode({self.text}, {self.text_type}, {self.url})"

def split_nodes_delimiter(old_nodes, delimiter, text_type):
 new_nodes = []
 for node in old_nodes:
  if node.text_type != text_type_text:
   new_nodes += [node]
  elif len(node.text.split(delimiter)) % 2 == 0 :
   raise Exception("Inalid markdown")
  else :
   text = node.text.split(delimiter)
   for i in range(len(text)):
    if text[i] == "":
     continue
    if i % 2 == 1:
     new_nodes.append(TextNode(text[i], text_type))
    else :
     new_nodes.append(TextNode(text[i], text_type_text))
 return new_nodes
    
def extract_markdown_images(text):
 return re.findall(r"!\[(.*?)\]\((.*?)\)", text)
 
def extract_markdown_links(text):
 return re.findall(r"\[(.*?)\]\((.*?)\)", text)

def split_nodes_image(old_nodes):
 new_nodes = []
 def inner(text):
  tupsImg = extract_markdown_images(text)
  
  start, end = "", text
  result = []
  
  for content, url in tupsImg:
   start, end = end.split(f"![{content}]({url})")
   if start != "":
    result += [TextNode(start, text_type_text)]
   result += [TextNode(content, text_type_image, url)]
  
  if end != "":
   result += [TextNode(end, text_type_text)]
  
  return result
  
 for node in old_nodes:
  if extract_markdown_images(node.text) == []:
   new_nodes += [node]
  else :
   new_nodes += inner(node.text)
 
 return new_nodes
  
  
def split_nodes_link(old_nodes):
 new_nodes = []
 def inner(text):
  tupsLink = extract_markdown_links(text)
  
  start, end = "", text
  result = []
  
  for content, url in tupsLink:
   start, end = end.split(f"[{content}]({url})")
   if start != "":
    result += [TextNode(start, text_type_text)]
   result += [TextNode(content, text_type_link, url)]
  
  if end != "":
   result += [TextNode(end, text_type_text)]
  
  return result
  
 for node in old_nodes:
  if extract_markdown_links(node.text) == []:
   new_nodes += [node]
  else :
   new_nodes += inner(node.text)
 
 return new_nodes
 
 
def text_to_textnodes(text):
 nodes = [TextNode(text, text_type_text)]
 nodes = split_nodes_delimiter(nodes, "**", text_type_bold)
 nodes = split_nodes_delimiter(nodes, "*", text_type_italic)
 nodes = split_nodes_delimiter(nodes, "`", text_type_code)
 nodes = split_nodes_image(nodes)
 nodes = split_nodes_link(nodes)
 
 return nodes