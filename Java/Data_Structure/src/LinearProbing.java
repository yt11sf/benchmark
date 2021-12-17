
public class LinearProbing {
	private Student[] table;
	private int counter, size;

	public LinearProbing(int arraySize) {
		table = new Student[arraySize];
	}

	public int getTableSize() {
		return table.length;
	}
	public int getSize() {
		return size;
	}

	public boolean insert(Student stud) {
		int index = stud.hashing(stud.getId(), table.length);
		if (table[index] == null) {
			table[index] = stud;
			size++;
			return true;
		} else {
			counter = 0;
			while (true) {
				counter++;
				if (counter > table.length)
					return false;
				if (++index > table.length - 1)
					index = 0;
				if (table[index] == null){
					table[index] = stud;
					size++;
					return true;
				}
			}
		}
	}

	public Student search(int id) {
		Student stud = new Student();
		counter = 0;
		for (int n = stud.hashing(id, table.length); n < table.length; n++) {
			counter++;
			if (counter > table.length)
				return null;
			if (table[n] != null)
				if (id == table[n].getId())
					return table[n];
		}
		return null;
	}

	public boolean delete(int id) {
		Student stud = new Student();
		counter = 0;
		for (int n = stud.hashing(id, table.length); n < table.length; n++) {
			counter++;
			if (counter > table.length)
				return false;
			if (table[n] != null)
				if (id == table[n].getId()) {
					table[n] = null;
					size--;
					return true;
				}
		}
		return false;
	}

	public void print() {
		counter = 0;
		for (Student student : table)
			if (student != null) {
				System.out.println(++counter + ".\t" + student);
			}
	}

	public Student retrieveToCopy(int counter) {
		int counter2 = 0;
		Student stud = new Student();
		for (Student student : table) {
			if (student != null) {
				counter2++;
				if (counter == counter2)
					return student;
			}
		}
		return null;
	}
}
