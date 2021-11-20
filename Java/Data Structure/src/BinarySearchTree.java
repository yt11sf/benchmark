
public class BinarySearchTree {
	private TreeNode[] table;
	int counter;

	public BinarySearchTree(int arraySize) {// Constructor
		table = new TreeNode[arraySize];
	}

	public boolean insert(Student stud) {// Insert Student
		return (table[stud.hashing(stud.getId(), table.length)] = insert(stud,
				table[stud.hashing(stud.getId(), table.length)])) != null;
	}

	private TreeNode insert(Student stud, TreeNode node) {// Insert Student (private recursive)
		if (node == null)
			node = new TreeNode(stud);
		else {
			if (stud.getId() <= node.stud.getId())
				node.left = insert(stud, node.left);
			else
				node.right = insert(stud, node.right);
		}
		return node;
	}

	public TreeNode search(int id) {// Search Student
		Student stud = new Student();
		TreeNode root = table[stud.hashing(id, table.length)];
		if(root == null)
			return null;
		return search(id, root);
	}

	private TreeNode search(int id, TreeNode node) {// Search Student (private recursive)
		if (node != null)
			if (id == node.stud.getId())
				return node;
			else if (id < node.stud.getId())
				return search(id, node.left);
			else
				return search(id, node.right);
		else
			return null;
	}

	public boolean delete(int id) {// Delete Student
		Student stud = new Student();
		TreeNode root = table[stud.hashing(id, table.length)];
		if (search(id) == null)
			return false;
		table[stud.hashing(id, table.length)] = delete(id, root);
		return true;
	}

	private TreeNode delete(int id, TreeNode node) {// Delete Student (private recursive)
		if (node.stud.getId() == id) {// id match
			if (node.left == null && node.right == null)
				return null;
			else if (node.left == null)
				return node.right;
			else if (node.right == null)
				return node.left;
			else {
				TreeNode temp = node.right;
				while (node.right.left != null)
					node.right = node.right.left;
				node.right.left = node.left;
				return temp;
			}
		} else if (id < node.stud.getId()) {
			TreeNode temp = delete(id, node.left);
			node.left = temp;
		} else {
			TreeNode temp = delete(id, node.right);
			node.right = temp;
		}
		return node;
	}

	public void print() { // Print BST
		counter = 0;
		for (TreeNode treeNode : table) postOrder(treeNode);
	}

	private void postOrder(TreeNode temp) {// Print BST in Post Order
		if (temp != null) {
			postOrder(temp.left);
			postOrder(temp.right);
			counter++;
			System.out.println(counter + ".\t" + temp.stud.toString());
		}
	}
}

class TreeNode {
	TreeNode left, right;
	Student stud;

	public TreeNode(Student stud) {// constructor
		left = right = null;
		this.stud = stud;
	}
}
