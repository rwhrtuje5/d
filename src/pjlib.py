from htmlnode import *
from textnode import *
from block import *
from OwnCopyTree import *


def text_node_to_html_node(tNode):
 if tNode.text_type not in ACCEPTABLE_TEXT_TYPE:
  raise Exception(f'{tNode} type invalid')
 match tNode.text_type:
  case "text":
   return LeafNode(None, tNode.text)
  case "bold":
   return LeafNode("b", tNode.text)
  case "italic":
   return LeafNode("i", tNode.text)
  case "code":
   return LeafNode("code", tNode.text)
  case "link":
   return LeafNode("a", tNode.text, {"href":tNode.url})
  case "image":
   return LeafNode("img", "",{"src":tNode.url, "alt":tNode.text})

def textnodes_to_html_nodes(tNodes):
 return [text_node_to_html_node(node) for node in tNodes]

def markdown_to_html_node(markdown):
 blocks = markdown_to_blocks(markdown)
 html = ParentNode("div", [])
 for block in blocks:
  match block_to_block_type(block):
   case "quote":
    lines = block.split("\n")
    block = ParentNode("blockquote", []) 
    for line in lines:
     block.children += textnodes_to_html_nodes(text_to_textnodes(line[1:]))
    html.children.append(block)
   
   case "ordered_list":
    lines = block.split("\n")
    block = ParentNode("ol", [])
    for line in lines:
     block.children.append(ParentNode("li", textnodes_to_html_nodes(text_to_textnodes(" ".join(line.split()[1:])))))
    html.children.append(block)
    
   case "unordered_list":
    lines = block.split("\n")
    block = ParentNode("ul", [])
    for line in lines:
     block.children.append(ParentNode("li", textnodes_to_html_nodes(text_to_textnodes(line[1:]))))
    html.children.append(block)
   
   case "code":
    block = ParentNode('pre', [LeafNode('code', block.strip('`'))])
    html.children.append(block)
   
   case "heading":
    leveling = lambda s: len(s.split()[0])
    block = LeafNode(f'h{leveling(block)}', ' '.join(block.split()[1:]))
    html.children.append(block)
    
   case _:
    block = ParentNode("p", textnodes_to_html_nodes(text_to_textnodes(block)))
    
    html.children.append(block)
    
 return html   
 
 
def extract_title(markdown):
 markdown = markdown.split("\n")
 for line in markdown:
  if line.startswith("# "):
   return line[2:]
 
 raise Exception("All pages need a single h1 header")
 
def generate_page(from_path, template_path, dest_path):
 content = ""
 template = ""
 
 with open(from_path) as file:
  content = file.read()
 
 with open(template_path) as file:
  template = file.read()
 
 if not os.path.exists(join_paths(dest_path.split("/")[:-1])):
  os.makedirs(join_paths(dest_path.split("/")[:-1]))
 
 html_node = markdown_to_html_node(content)
 
 html = template.replace("{{ Title }}", extract_title(content)).replace("{{ Content }}", html_node.to_html())
 
 with open(dest_path, "w") as file:
  file.write(html)
  
  
def generate_pages_recursive(src, dst, template_path = ""):
 mkdir(dst)
 for file in os.listdir(src):
  os.system(f"cp -r {join_paths([src, file])} {dst}")
 
 def dfs(path):
  if os.path.isfile(path):
   if path[-3:] == ".md":
    generate_page(path, template_path, path)
    os.system(f"mv {path} {path[:-3] + '.html'}")    
  else :
   for f in os.listdir(path):
    dfs(os.path.join(path, f))
 
 dfs(dst)