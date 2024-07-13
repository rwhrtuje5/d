class HTMLNode:
 def __init__(self, tag = None, val = None, children = None, props = None):
  self.tag = tag  
  self.value = val  
  self.children = children
  self.props = props
 
 
 def to_html(self):
  raise NotImplementedError("to_html method not implemented")
  
  
 def props_to_html(self):
  if self.props == None:
   return ""
  html = ""
  for at in self.props:
   html += f" {at}=\"{self.props[at]}\""
  
  return html
  
 def __repr__(self):
  return f"HTMLNode<tag:{self.tag}, value:{self.value}, children:{self.children}, props:{self.props}>"

  
class LeafNode(HTMLNode):
 def __init__(self, tag, val, props = None):
  super().__init__(tag, val, None, props)
  
 def to_html(self):
  if self.value == None:
   raise ValueError(f"ValueError: All leaf nodes require a value")
  if self.tag is None:
    return self.value
  return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
  
 def __repr__(self):
  return f"LaefNode<tag:{self.tag}, value:{self.value}, props:{self.props}>"


class ParentNode(HTMLNode):
 def __init__(self, tag = None, children = None, props = None):
  super().__init__(tag, None, children, props)
 
 def to_html(self):
  if self.tag == None:
   raise ValueError("Tag wasnt provide")
  if self.children == None:
   raise ValueError("No children")
   
  html = ""
  for child in self.children:
   html += child.to_html() + "\n"
  
  html = f"<{self.tag}{self.props_to_html()}>\n" + html + f"</{self.tag}>"
  
  return html
  
  
  def __repr__(s):
   return f"ParentNode<tag:{self.tag}, children:{self.children}, props:{self.props}>"
  