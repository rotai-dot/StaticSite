class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props


    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if not self.props:
            return ""

        formatted_output = ""
        for key, value in self.props.items():
            formatted_output += (f' {key}="{value}"')

        return formatted_output

    def __repr__(self):
        return f"HTMLNode({self.tag!r}, {self.value!r}, {self.children!r}, {self.props!r})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value = value, props = props)

    def to_html(self):
        if self.value == None:
            raise ValueError
        if not self.tag:
            return self.value
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'

    def __repr__(self):
            return f"LeafNode({self.tag!r}, {self.value!r}, {self.props!r})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag=tag, children = children, props=props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("Tag is needed")
        if self.children == None:
            raise ValueError("Children are needed")

        result=""
        for child in self.children:
            result += child.to_html()

        return  f'<{self.tag}{self.props_to_html()}>{result}</{self.tag}>'     
        