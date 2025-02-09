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
        
