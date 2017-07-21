class Animal {
  /* gradual typing means this is "optional".  But the linter will warn */
  var name: str;
  var age: int;

  def __init__(self, name: str, age: int) {
    self.name = name;
    self.age = age;
  }

  def __str__(self) -> str {
    "an animal named {}".format(self.name)
  }

  def __repr__(self) -> str {
    "<Animal {:?}>".format(self.name)
  }
}

class Dog(Animal) {
  var is_barking: bool;

  def __init__(self, name: str, age: int) {
    Animal.__init__(self, name, age);
    self.is_barking = false;
  }
}

def main() {
  var items = [
    Dog('Lumpi', 3),
    Dog('Joe', 7),
  ];

  for item in items {
    println("I have {}; it is {} years old", item, item.age);
  }
}
