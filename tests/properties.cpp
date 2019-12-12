#include "properties.h"

int Something::get_value() const { return m_value; }
void Something::set_value(int value) { m_value = value; }
bool Something::computed() const { return true; }
int Something::get_other() const { return m_other; }
void Something::set_other(int value) { m_other = value; }
int Something::get_overloaded() const { return m_overloaded; }
int Something::get_overloaded(Argument /*ignored*/) const {
  return m_overloaded;
}
void Something::set_overloaded(int value) { m_overloaded = value; }
void Something::set_overloaded(Argument /*ignored*/) { m_overloaded = 0; }
