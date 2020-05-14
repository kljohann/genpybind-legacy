#pragma once

#include <iostream>
#include <memory>
#include <pybind11/pybind11.h>
#include "genpybind.h"

int& get_global_instance_counter() GENPYBIND(visible)
{
	static int global_instance_counter = 42;
	return global_instance_counter;
}

class GENPYBIND(hidden) RAII
{
public:
	RAII() {
		get_global_instance_counter()++;
	}
	~RAII() {
		get_global_instance_counter()--;
	}
};

class GENPYBIND(visible) ProxyRAII
{
public:
	ProxyRAII() = default;

	void __enter__() {
		m_raii_inst.reset(new RAII);
	}

	void __exit__(pybind11::object exc_type,
	              pybind11::object exc_value,
	              pybind11::object traceback) {
		m_raii_inst.reset();
	}

private:
	std::unique_ptr<RAII> m_raii_inst;
};
