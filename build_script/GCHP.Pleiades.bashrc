#!/bin/bash
# Builds NetCDF on Pleiades using the standard compiler set, ready for GCHP
module purge
#module load git/2.4.5
module load comp-intel/2015.3.187

# Pleiades' native SGI MPI - default
module load mpi-sgi/mpt
export ESMF_COMM=mpi

# If you want to use MVAPICH2 instead, comment out the 2 lines above and uncomment these lines
#module load mpi-mvapich2/2.0/intel
#export ESMF_COMM=mvapich2

# Tell GCHP where the MPI binaries, libraries and so on can be found
#export MPI_ROOT=$( dirname $( dirname $( which mpirun ) ) )
export MPI_ROOT=$( dirname $( dirname $( which mpiexec ) ) )

# Set up the compilers
export FC=ifort
export F90=$FC
export F9X=$FC
export F77=$FC
export CC=gcc
export CXX=g++

# This needs to be the location where NetCDF-C and NetCDF-Fortran were installed
installDir=$HOME/local

# Needed one NetCDF is installed
export NETCDF_HOME=$installDir

export GC_BIN="$NETCDF_HOME/bin"
export GC_INCLUDE="$NETCDF_HOME/include"
export GC_LIB="$NETCDF_HOME/lib"

# Add NetCDF to path
export PATH=$PATH:${NETCDF_HOME}/bin
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:${NETCDF_HOME}/lib

# Disable OpenMP
export OMP_NUM_THREADS=1
