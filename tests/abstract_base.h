#pragma once

#include "genpybind.h"

struct GENPYBIND(visible) AbstractBase {
	virtual int whatever(int value) const;
	virtual int something(int value) const;
	virtual double return_magic_number() const = 0;
	virtual ~AbstractBase() = default;

	static bool static_method();
};

struct GENPYBIND(visible) Derived : public AbstractBase {
	int something(int value) const override;
	double return_magic_number() const override;
};
