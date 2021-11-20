
public class MultiLayeredHashing {
	private Student[][] table;
	private int counter, counter2;

	public MultiLayeredHashing(int arraySize, int secArraySize) {
		table = new Student[arraySize][secArraySize];
	}

	public boolean insert(Student stud) {
		int index1 = stud.hashing(stud.getId(), table.length),
				index2 = stud.hashing2(stud.getName(), table[index1].length);
		if (table[index1][index2] == null) {
			table[index1][index2] = stud;
			return true;
		} else {
			counter2 = 0;
			while (true) {
				counter = 0;
				counter2++;
				if (counter2 > table.length)
					return false;
				while (true) {
					counter++;
					if (counter > table[index1].length) break;
					if (++index2 > table[index1].length - 1) index2 = 0;
					if (table[index1][index2] == null){
						table[index1][index2] = stud;
						return true;
					}
				}
				if (++index1 > table.length - 1) index1 = 0;
			}
		}
	}

	public Student search(int id, String name) {
		Student stud = new Student();
		counter2 = 0;
		int index1 = stud.hashing(id, table.length), index2 = stud.hashing2(name, table[index1].length);
		if (table[index1][index2] == null)
			return null;
		while (true) {
			counter2++;
			if (counter2 > table.length)
				return null;
			counter = 0;
			while (true) {
				counter++;
				if (counter > table[index1].length)
					break;
				if (table[index1][index2] != null) 
					if (table[index1][index2].getId() == id) 
						return table[index1][index2];	
				if (++index2 == table[index1].length)
					index2 = 0;
			}
			if (++index1 == table.length)
				index1 = 0;
		}
	}
	public boolean delete(int id, String name) {
		Student stud = new Student();
		counter2 = 0;
		int index1 = stud.hashing(id, table.length), index2 = stud.hashing2(name, table[index1].length);
		if (table[index1][index2] == null)
			return false;
		while (true) {
			counter2++;
			if (counter2 > table.length)
				return false;
			counter = 0;
			while (true) {
				counter++;
				if (counter > table[index1].length)
					break;
				if (table[index1][index2] != null) 
					if (table[index1][index2].getId() == id) {
						table[index1][index2] = null;
						return true;	
					}
				if (++index2 == table[index1].length)
					index2 = 0;
			}
			if (++index1 == table.length)
				index1 = 0;
		}
	}

	public void print() {
		counter = 0;
		for (Student[] students : table)
			for (Student student : students)
				if (student != null) System.out.println(++counter + ".\t" + student);
	}
}
