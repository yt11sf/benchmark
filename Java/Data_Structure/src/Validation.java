import java.util.Scanner;

public class Validation {
	public boolean isDigit(String digit) {// Validate Entry with Digits Only
		if(digit == null || digit.trim().isEmpty())
			return false;
		for (int n = 0; n < digit.length(); n++)
			if (!Character.isDigit(digit.charAt(n)))
				return false;
		return true;
	}

	public boolean isLetter(String letter) {// Validate Entry with Letters AND/OR Space
		if(letter == null || letter.trim().isEmpty())
			return false;
		for (int n = 0; n < letter.length(); n++)
			if (!Character.isLetter(letter.charAt(n)) && !Character.isSpace(letter.charAt(n))) {
				System.err.println("Invalid Name: Only Letters or Space is Allowed");
				return false;
			}
		return true;
	}

	public int getValidID() {// Prompt Student ID Input
		Scanner input = new Scanner(System.in);
		while (true) {
			System.out.println("Enter ID OR Any Other Character to Exit (1 ~ 99999)");
			String id = input.nextLine();
			if (!isDigit(id))
				return 0;
			else if (Integer.parseInt(id) > 99999 || Integer.parseInt(id) < 1) {
				System.out.println("Please Enter Valid ID (1 ~ 99999)");
			} else
				return Integer.parseInt(id);
		}
	}

	public String getValidName() {// Prompt Student Name Input
		Scanner input = new Scanner(System.in);
		System.out.println("Enter Name OR Any Characters Other Than Letter AND/OR Space to Exit");
		String name = input.nextLine();
		if (!isLetter(name))
			return null;
		return name;
	}
}
