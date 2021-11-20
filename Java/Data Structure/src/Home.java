import java.util.Random;
import java.util.Scanner;

public class Home {
	private static int id;
	private static final int arraySize = 100, secArraySize = 100;
	private static String name, idStr;
	private static BinarySearchTree tree = new BinarySearchTree(arraySize);
	private static LinearProbing lp = new LinearProbing(arraySize);
	private static MultiLayeredHashing ml = new MultiLayeredHashing(arraySize, secArraySize);

	public static void main(String[] args) {
		Validation valid = new Validation();
		Scanner input = new Scanner(System.in);
		long start, stop = 0;
		boolean success = false;
		int n = 0;
		while (n == 0) {
			System.out
					.println("Select Function: (Exit by entering other than 1~7)\n1.\tInsert\n2.\tSearch\n3.\tDelete\n"
							+ "4.\tLinear Probing Traversal\n5.\tBinary Search Tree Traversal\n6.\tMulti-Layered Hashing Traversal\n"
							+ "7.\tDelete ALL");
			String function = input.nextLine();
			switch (function) {
			case "1":
				System.out.println("Auto Generate Students?\n1.\tYESS!\n2.\tno? (Insertion Time Check)");
				String auto = input.nextLine();
				if (auto.equals("1")) {
					while (true) {
						System.out.println("Generate How Many Students?");
						String num = input.nextLine();
						if (valid.isDigit(num)) {
							generateRandom(Integer.parseInt(num));
							break;
						} else
							System.out.println("Enter Digits Only");
					}
				} else if (auto.equals("2")) {
					while (true) {
						if ((id = valid.getValidID()) == 0)
							break;
						if ((name = valid.getValidName()) == null)
							break;
						idStr = String.format("%5d", id).replace(' ', '0');// left pad with 0
						Student stud = new Student(idStr, name);
						if (tree.search(id) != null) {
							System.out.println("ID " + idStr + " has been Taken");
							continue;
						}
						// Open Addressing - Linear Probing (constant)
						start = System.nanoTime();
						success = lp.insert(stud);
						stop = System.nanoTime();
						if (!success)
							if (lp.getSize() < lp.getTableSize())
								System.out.println("Insertion Failed in Linear Probing: " + stud.getIdStr());
							else {// Table Full --> Reconstruct Table
								System.out.println("Table of Linear Probing Fulled");
								reconstructLP(50);
								if (!lp.insert(stud))
									System.out.println("Insertion Failed After Reconstruct");
								stop = System.nanoTime();
							}
						System.out.println("Linear Probing Insert Time: " + (stop - start) + "ns");
						
						// Separate Chaining with Binary Search Tree
						start = System.nanoTime();
						success = tree.insert(stud);
						stop = System.nanoTime();
						if (!success)
							System.out.println("Insertion Failed in Binary Search Tree");
						System.out.println("Binary Search Tree Insert Time: " + (stop - start) + "ns");

						// Multi-Layered Hashing: Might work well with HUGE data base
						start = System.nanoTime();
						success = ml.insert(stud);
						stop = System.nanoTime();
						if (!success)
							System.out.println("Insertion Failed in Multi-Layered Hashing");
						System.out.println("Multi-Layered Hashing Insert Time: " + (stop - start) + "ns");

						System.out.println("Continue to Insert Press ENTER");
						String con = input.nextLine();
						if (!con.equals(""))
							break;
					}
				}
				break;
			case "2":
				id = valid.getValidID();
				if (id == 0)
					break;

				// Linear Probing
				System.out.println("Linear Probing");
				start = System.nanoTime();
				Student temp = lp.search(id);
				stop = System.nanoTime();
				if (temp != null) {
					System.out.println(temp.toString() + "\nSearch Time: " + (stop - start) + " ns");
				} else
					System.out.println("ID " + id + " Not Found\nSearch Time: " + (stop - start) + " ns");
				System.out.println();

				// Binary Search Tree
				System.out.println("Binary Search Tree");
				start = System.nanoTime();
				TreeNode temp2 = tree.search(id);
				stop = System.nanoTime();
				if (temp2 != null) {
					System.out.println(temp2.stud.toString() + "\nSearch Time: " + (stop - start) + " ns");
				} else
					System.out.println("ID " + id + " Not Found\nSearch Time: " + (stop - start) + " ns");
				System.out.println();

				// Multi-Layered Hashing
				System.out.println("Enter Name for Multi-Layered Hashing");
				name = valid.getValidName();
				if (name == null)
					break;
				start = System.nanoTime();
				Student temp3 = ml.search(id, name);
				stop = System.nanoTime();
				if (temp3 != null) {
					System.out.println(temp3.toString() + "\nSearch Time: " + (stop - start) + " ns");
				} else
					System.out.println("ID " + id + " Not Found\nSearch Time: " + (stop - start) + " ns");
				System.out.println();
				break;
			case "3":
				id = valid.getValidID();
				if (id == 0)
					break;
				start = System.nanoTime();
				boolean out = lp.delete(id);
				stop = System.nanoTime();
				System.out.println("Linear Probing: " + out + "\nSearch Time: " + (stop - start) + " ns");
				start = System.nanoTime();
				out = tree.delete(id);
				stop = System.nanoTime();
				System.out.println("Binary Search Tree: " + out + "\nSearch Time: " + (stop - start) + " ns");
				System.out.println();
				System.out.println("Enter Name for Multi-Layered Hashing");
				name = valid.getValidName();
				if (name == null)
					break;
				start = System.nanoTime();
				out = ml.delete(id, name);
				stop = System.nanoTime();
				System.out.println("Multi-Layered Hashing: " + out + "\nSearch Time: " + (stop - start) + " ns");
				System.out.println();
				break;
			case "4":
				lp.print();
				System.out.println();
				break;
			case "5":
				tree.print();
				System.out.println();
				break;
			case "6":
				ml.print();
				System.out.println();
				break;
			case "7":
				lp = new LinearProbing(arraySize);
				tree = new BinarySearchTree(arraySize);
				ml = new MultiLayeredHashing(arraySize, secArraySize);
				System.out.println("Entries Cleared");
				break;
			default:
				n++;
			}
			System.gc();
		}
		input.close();
		System.out.println("Program EXITED");
	}

	private static void generateRandom(int num) {
		for (int h = 0; h < num; h++) {
			generateRandom();
			Student stud = new Student(idStr, name);
			if (tree.search(id) != null) {
				h--;
				continue;
			}

			// Open Addressing - Linear Probing (constant)
			if (!lp.insert(stud))
				if (lp.getSize() < lp.getTableSize())
					System.out.println("Insertion Failed in Linear Probing: " + stud.getIdStr());
				else {// Table Full --> Reconstruct Table
					System.out.println("Table of Linear Probing Fulled");
					reconstructLP(num);
					if (!lp.insert(stud))
						System.out.println("Insertion Failed After Reconstruct");
				}

			// Separate Chaining with Binary Search Tree
			if (!tree.insert(stud))
				System.out.println("Insertion Failed in Binary Search Tree: " + stud.getIdStr());

			// Multi-Layered Hashing
			if (!ml.insert(stud))
				System.out.println("Insertion Failed in Multi-Layered Hashing: " + stud.getIdStr());
		}
	}

	private static void generateRandom() {// Generate Random Student Registry
		Random r = new Random();
		do {
			name = "";
			id = (int) (r.nextInt(99999));
			for (int k = 0; k < 5; k++)
				name += (char) (r.nextInt('z' - 'a') + 'a');
		} while (id > 99999);
		idStr = String.format("%5d", id).replace(' ', '0');// left pad with 0
	}

	private static void reconstructLP(int num) {// Resize Table in Linear Probing
		System.out.println("Reconstructing Table");
		long start = 0, stop = 0;
		start = System.nanoTime();
		LinearProbing temp = lp;
		lp = new LinearProbing(lp.getSize() + (num * 2));
		int counter = 0;
		for (int n = 0; n < temp.getSize(); n++)
			lp.insert(temp.retrieveToCopy(++counter));
		stop = System.nanoTime();
		System.out.println("Table Reconstructed\nTime Consumed: " + (stop - start) + "ns");// Consumed
	}
}
