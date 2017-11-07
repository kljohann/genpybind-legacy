#include "enums.h"

std::string test_enum(State state) {
  switch (state) {
  case YES:
    return "Yes";
  case NO:
    return "No";
  case MAYBE:
    return "Maybe";
  default:
    return "?";
  }
}

std::string test_enum(Color color) {
  switch (color) {
  case Color::red:
    return "red";
  case Color::green:
    return "green";
  case Color::blue:
    return "blue";
  default:
    return "?";
  }
}
