cmake_minimum_required(VERSION 3.11)
project(python-call VERSION 1.0.0 LANGUAGES CXX)

# Python is required for this project
#   - we also use python `requests` module
find_package (Python REQUIRED 
    COMPONENTS Interpreter Development
)

message(" -------------------------------------------------------------------------------------- ")
message(" -- Python FOUND")
message(" --     Python_EXECUTABLE           = ${Python_EXECUTABLE}")
message(" --     Python_Compiler_FOUND       = ${Python_Compiler_FOUND}")
message(" --     Python_INCLUDE_DIRS         = ${Python_INCLUDE_DIRS}")
message(" --     Python_LIBRARIES            = ${Python_LIBRARIES}")
message(" --     Python_LINK_OPTIONS         = ${Python_LINK_OPTIONS}")
message(" --     Python_LIBRARY_DIRS         = ${Python_LIBRARY_DIRS}")
message(" --     Python_RUNTIME_LIBRARY_DIRS = ${Python_RUNTIME_LIBRARY_DIRS}")
message(" -------------------------------------------------------------------------------------- ")

###############################################################################
# set sources
###############################################################################
file(GLOB_RECURSE ALL_SOURCES
    src/cpp/*.cpp
    src/cpp/*.h
)

# main executable
add_executable(${PROJECT_NAME}
    ${ALL_SOURCES}
)


# include directories
target_include_directories(${PROJECT_NAME} PRIVATE
    ${Python_INCLUDE_DIRS}
)

# link directories
target_link_directories(${PROJECT_NAME} PRIVATE
    ${Python_LIBRARY_DIRS}
)

# link libraries
target_link_libraries(${PROJECT_NAME} PRIVATE
    ${Python_LIBRARIES}
)