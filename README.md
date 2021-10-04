# .klank  (klank-lang)
 
## What's klank?
**klank** is an experimental **interpreted programming language based on python** I'm working on as an amusement project.
I'm trying to make it look fancy on github so I can use it professionally in my portfolio if it goes somewhere maybe?
However becareful on this projet, it's very much s**t

## What can klank do so far?
**klank, so far, can:**
* `var ;`: Create primitve vars types such as integers and strings. vars are subject to primitive operations (`+`, `-`)
* `print();`: You can print anything in the console: vars, ints, strings (ofc)
* `if() {}`: Run a code under a condition ( `==`, `!=`, `>`, `<`, `%=`)
* `else {}`: If the above if statement was false, then run this part of code
* `while() {}`: While the condition in the paranthesis is true, it will run the englobed code

## An example for the record?
This is a "fizzbuzz" game made in klank
The goal of fizzbuzz is to say "fizz" if the number is a multiple of 3, "buzz" if it's a multiple of 5, and "fizzbuzz" if both.
```klank
var i = 0;
var max = 100;

while (i < max) {
	i = i + 1;
	if (i %= 3) {
		if (i %= 5) {
			print("fizzbuzz");
		}
		else {
			print("fizz");
		}
	}
	else {
		if (i %= 5) {
			print("buzz");
		}
		else {
			print(i);
		}
	}
}
```