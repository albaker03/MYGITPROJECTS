import random
import string
import os
from datetime import datetime


class PasswordGenerator:
    """A robust password generator with customizable options."""
    
    def __init__(self):
        """Initialize character sets and default options."""
        self.lowercase = string.ascii_lowercase
        self.uppercase = string.ascii_uppercase
        self.digits = string.digits
        self.symbols = '!@#$%^&*()_+-=[]{}|;:,.<>?/'
        self.passwords = [] # List of generated passwords
    
    def get_positive_integer(self, prompt, min_val=1, max_val=None):
        """
        Get validated positive integer input from user.
        
        Args:
            prompt: Input prompt message
            min_val: Minimum acceptable value (default: 1)
            max_val: Maximum acceptable value (default: None)
        
        Returns:
            Valid integer value
        """
        while True:
            try:
                value = int(input(prompt))
                if value < min_val:
                    print(f"❌ Error: Value must be at least {min_val}.")
                    continue
                if max_val and value > max_val:
                    print(f"❌ Error: Value cannot exceed {max_val}.")
                    continue
                return value
            except ValueError:
                print("❌ Error: Please enter a valid whole number.")
            except KeyboardInterrupt:
                print("\n\nOperation cancelled by user.")
                return None
    
    def get_yes_no(self, prompt):
        """
        Get yes/no confirmation from user.
        
        Args:
            prompt: Question to ask
        
        Returns:
            Boolean value
        """
        while True:
            response = input(prompt).lower().strip()
            if response in ['yes', 'y']:
                return True
            elif response in ['no', 'n']:
                return False
            else:
                print("❌ Please enter 'yes' or 'no'.")
    
    def build_character_set(self):
        """
        Build character set based on user preferences.
        
        Returns:
            String containing all selected character types
        """
        char_set = ''
        
        print("\n" + "="*50)
        print("CHARACTER TYPE SELECTION")
        print("="*50)
        
        if self.get_yes_no("Include lowercase letters (a-z)? (yes/no): "):
            char_set += self.lowercase
            print("✓ Lowercase letters added")
        
        if self.get_yes_no("Include uppercase letters (A-Z)? (yes/no): "):
            char_set += self.uppercase
            print("✓ Uppercase letters added")
        
        if self.get_yes_no("Include numbers (0-9)? (yes/no): "):
            char_set += self.digits
            print("✓ Numbers added")
        
        if self.get_yes_no("Include special symbols (!@#$%...)? (yes/no): "):
            char_set += self.symbols
            print("✓ Special symbols added")
        
        if not char_set:
            print("\n❌ Error: You must select at least one character type!")
            return self.build_character_set()
        
        return char_set
    
    def calculate_strength(self, password_length, char_set_size):
        """
        Calculate password strength indicator.
        
        Args:
            password_length: Length of password
            char_set_size: Number of character types available
        
        Returns:
            Strength rating as string
        """
        if password_length < 8:
            return "⚠️  Weak"
        elif password_length < 12:
            if char_set_size < 3:
                return "⚠️  Fair"
            return "✓ Good"
        else:
            if char_set_size < 3:
                return "✓ Good"
            return "✓✓ Strong"
    
    def generate_password(self, length, char_set):
        """
        Generate a single password.
        
        Args:
            length: Password length
            char_set: String of characters to choose from
        
        Returns:
            Generated password string
        """
        password = ''.join(random.choice(char_set) for _ in range(length))
        return password
    
    def generate_passwords(self, count, length, char_set):
        """
        Generate multiple passwords.
        
        Args:
            count: Number of passwords to generate
            length: Length of each password
            char_set: String of characters to choose from
        
        Returns:
            List of generated passwords
        """
        self.passwords = [self.generate_password(length, char_set) for _ in range(count)]
        return self.passwords
    
    def display_passwords(self, length, char_set_size):
        """Display generated passwords with formatting."""
        print("\n" + "="*50)
        print("GENERATED PASSWORDS")
        print("="*50)
        
        strength = self.calculate_strength(length, char_set_size)
        print(f"Password Strength: {strength}\n")
        
        for idx, password in enumerate(self.passwords, 1):
            print(f"{idx:2d}. {password}")
        
        print("="*50)
    
    def save_passwords_to_file(self):
        """Save generated passwords to a file."""
        if not self.passwords:
            print("No passwords to save.")
            return
        
        if not self.get_yes_no("\nSave passwords to file? (yes/no): "):
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"passwords_{timestamp}.txt"
        
        try:
            with open(filename, 'w') as f:
                f.write(f"Generated Passwords - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("="*50 + "\n\n")
                for idx, password in enumerate(self.passwords, 1):
                    f.write(f"{idx}. {password}\n")
                f.write("\n" + "="*50 + "\n")
                f.write("⚠️  KEEP THIS FILE SECURE AND DELETE AFTER USE\n")
            
            print(f"✓ Passwords saved to {filename}")
        except IOError as e:
            print(f"❌ Error saving file: {e}")
    
    def copy_to_clipboard(self):
        """Copy a password to clipboard (requires pyperclip)."""
        if not self.passwords:
            return
        
        try:
            import pyperclip
            print("\nPasswords available:")
            for idx, password in enumerate(self.passwords, 1):
                print(f"{idx}. {password}")
            
            choice = self.get_positive_integer(
                "Enter password number to copy to clipboard (or 0 to skip): ",
                min_val=0,
                max_val=len(self.passwords)
            )
            
            if choice > 0:
                pyperclip.copy(self.passwords[choice - 1])
                print(f"✓ Password {choice} copied to clipboard!")
        except ImportError:
            print("\n💡 Tip: Install pyperclip for clipboard support: pip install pyperclip")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def run(self):
        """Main application loop."""
        print("\n" + "="*50)
        print("ADVANCED PASSWORD GENERATOR")
        print("="*50)
        
        try:
            # Get number of passwords
            num_passwords = self.get_positive_integer(
                "\nHow many passwords do you want to generate? (1-100): ",
                min_val=1,
                max_val=100
            )
            
            if num_passwords is None:
                return
            
            # Get password length
            password_length = self.get_positive_integer(
                "Enter desired password length (8-128 characters): ",
                min_val=8,
                max_val=128
            )
            
            if password_length is None:
                return
            
            # Build character set
            char_set = self.build_character_set()
            
            # Generate passwords
            print("\n🔄 Generating passwords...")
            self.generate_passwords(num_passwords, password_length, char_set)
            
            # Display results
            self.display_passwords(password_length, len(set(char_set)))
            
            # Save option
            self.save_passwords_to_file()
            
            # Copy option
            if self.get_yes_no("\nCopy a password to clipboard? (yes/no): "):
                self.copy_to_clipboard()
            
            # Continue prompt
            if self.get_yes_no("\nGenerate more passwords? (yes/no): "):
                self.run()
            else:
                print("\n✓ Thank you for using Advanced Password Generator!")
        
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
            print("Please try again.")


def main():
    """Main entry point."""
    generator = PasswordGenerator()
    generator.run()


if __name__ == "__main__":
    main()
