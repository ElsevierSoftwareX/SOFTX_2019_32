# suffix rules
.SUFFIXES: .o .f90 .F90
.f90.o:
	$(FC) -c $(CPP) $(OPT) $<

.F90.o:
	$(FC) -c $(CPP) $(OPT) $<

# Fortran Compiler 
FC = gfortran
#FC = xlf
#FC = ifort

OPT =
CPP = 
LDFLAGS =

TARGETS = geninit
all: $(TARGETS)

# explicit rules
geninit: geninit.o
	$(FC) -o $@ $^ $(LDFLAGS)
	./geninit 
	cp -v rxff.bin ../DAT

nocopy: geninit.o
	$(FC) -o $@ $^ $(LDFLAGS)
	./geninit

clean:
	rm -f all.bin rxff.bin ../DAT/rxff.bin geninit.xyz real.xyz norm.xyz *.o *.mod *.MOD $(TARGETS)
