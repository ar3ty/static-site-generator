from functools import reduce

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError("to_html method not yet implemented")
    
    def props_to_html(self):
        if self.props != None:
            tuple_props = self.props.items()
            return "".join([f' {key}="{value}"' for key, value in tuple_props])
        return ""
    
    def __eq__(self, other):
        return self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props

    def __repr__(self):
        return f"HTMLNode(Tag: {self.tag}, value: {self.value}, children: {self.children}, props: {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value == None:
            raise ValueError("should have a value")
        elif self.tag == None:
            return self.value
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'

    def __repr__(self):
        return f'LeafNode(Tag: {self.tag}, value: {self.value}, props: {self.props})'
        
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("should have a tag")
        elif self.children == None:
            raise ValueError("should have children objects")
        cat_chidren = reduce(lambda cat, child: cat + child.to_html(), self.children, "")
        return f'<{self.tag}{self.props_to_html()}>{cat_chidren}</{self.tag}>'
    
    def __repr__(self):
        return f'ParentNode(Tag: {self.tag}, children: {self.children}, props: {self.props})'