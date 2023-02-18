class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

    def display(self):
        lines, *_ = self._display_aux()
        for line in lines:
            print(line)

    def _display_aux(self):
        """Returns list of strings, width, height, and horizontal coordinate of the root."""
        # No child.
        if self.right is None and self.left is None:
            line = '%s' % self.data
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        # Only left child.
        if self.right is None:
            lines, n, p, x = self.left._display_aux()
            s = '%s' % self.data
            u = len(s)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
            second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
            shifted_lines = [line + u * ' ' for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        # Only right child.
        if self.left is None:
            lines, n, p, x = self.right._display_aux()
            s = '%s' % self.data
            u = len(s)
            first_line = s + x * '_' + (n - x) * ' '
            second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
            shifted_lines = [u * ' ' + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

        # Two children.
        left, n, p, x = self.left._display_aux()
        right, m, q, y = self.right._display_aux()
        s = '%s' % self.data
        u = len(s)
        first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s + y * '_' + (m - y) * ' '
        second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '
        if p < q:
            left += [n * ' '] * (q - p)
        elif q < p:
            right += [m * ' '] * (p - q)
        zipped_lines = zip(left, right)
        lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
        return lines, n + m + u, max(p, q) + 2, n + u // 2



def insertBST(root, node):
  if (node.data < root.data):
    if root.left is None:
      root.left = node
    else:
      insertBST(root.left, node)
  else:
    if root.right is None:
      root.right = node
    else:
      insertBST(root.right, node)

def preOrder(node):
  if not node:
    return
  print(node.data)
  preOrder(node.left)
  preOrder(node.right)

def inOrder(node):
  inorderArr = []

  if node.left is not None:
    leftInorderArr = inOrder(node.left)
    inorderArr.extend(leftInorderArr)

  inorderArr.append(node.data)

  if node.right is not None:
    rightInorderArr = inOrder(node.right)
    inorderArr.extend(rightInorderArr)
  return inorderArr

def depth(root):

  if root is None:
    return - 1
  leftAns = depth(root.left)
  rightAns = depth(root.right)

  return max(leftAns, rightAns) + 1

def BBT(sortedArr):
  if not sortedArr:
    return None

  mid = int((len(sortedArr)-1)/2)

  newRoot = Node(sortedArr[mid])
  newRoot.left = BBT(sortedArr[:mid])
  newRoot.right = BBT(sortedArr[mid + 1 :])

  return newRoot

def complete(node, sortedArr):
    if node is None:
        return
    if node.right is not None and node.left is None:
        node.left = Node(node.data)
        complete(node.right, sortedArr)
    elif node.right is None and node.left is None and node.data != sortedArr[-1]:
        node.left = Node(node.data)
        node.right = Node(sortedArr[sortedArr.index(node.data) + 1])
    else:
        complete(node.left, sortedArr)
        complete(node.right, sortedArr)


def main():
    b = Node(3)
    insertBST(b, Node(2))
    insertBST(b, Node(1))
    insertBST(b, Node(4))
    insertBST(b, Node(5))
    insertBST(b, Node(6))

    a = inOrder(b)
    c = BBT(a)
    c.display()

    complete(c, a)
    c.display()
    print(inOrder(c))

if __name__ == "__main__":
    main()