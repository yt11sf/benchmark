
public class Student {
	private String name, id;

	public Student() {
	}

	public Student(String id, String name) {
		this.id = id;
		this.name = name;
	}

	public int hashing(int id, int arrayLength) {
		return id % arrayLength;
	}

	public int hashing2(String name, int arrayLength) {
		int total = 0;
		for (int n = 0; n < name.length(); n++)
			total += name.charAt(n);
		return total % arrayLength;
	}

	public String getName() {
		return name;
	}

	public int getId() {
		return Integer.parseInt(id);
	}

	public String getIdStr() {
		return id;
	}

	public String toString() {
		return "ID: " + id + "\tName: " + name;
	}
}