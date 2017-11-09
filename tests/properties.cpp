#include "properties.h"

int Something::get_value() const { return m_value; }
void Something::set_value(int value) { m_value = value; }
bool Something::computed() const { return true; }
int Something::get_other() const { return m_other; }
void Something::set_other(int value) { m_other = value; }
