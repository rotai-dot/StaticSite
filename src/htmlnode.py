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
        print(f"tag = {self.tag}")
        print(f"value = {self.value}")
        print(f"children = {self.children}")
        print(f"props = {self.props}")


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
            print(f"tag = {self.tag}")
            print(f"value = {self.value}")
            print(f"props = {self.props}")