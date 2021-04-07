cmake_minimum_required(VERSION 3.11)
project(python-call VERSION 1.0.0 LANGUAGES CXX)

list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake")

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

###############################################################################
# post build custom commands to create a /bin test folder
###############################################################################

# create bin directory
add_custom_target(TARGET ${PROJECT_NAME} POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E make_directory ${CMAKE_SOURCE_DIR}/bin)

include(CopyUtils)

# copy executable to bin
COPY_FILE_IF_CHANGED(
    $<TARGET_FILE:${PROJECT_NAME}>
    ${CMAKE_SOURCE_DIR}/bin/$<TARGET_FILE_NAME:${PROJECT_NAME}>
    ${PROJECT_NAME}
)

# python scripts
COPY_DIRECTORY_IF_CHANGED(
    ${CMAKE_SOURCE_DIR}/src/python 
    ${CMAKE_SOURCE_DIR}/bin 
    ${PROJECT_NAME}
)

# bat scripts
COPY_FILE_INTO_DIRECTORY_IF_CHANGED(${CMAKE_SOURCE_DIR}/src/scripts/get_server_cert.bat 
    ${CMAKE_SOURCE_DIR}/bin 
    ${PROJECT_NAME}
)

# Vault
COPY_DIRECTORY_IF_CHANGED(
    ${CMAKE_SOURCE_DIR}/vault
    ${CMAKE_SOURCE_DIR}/bin/vault
    ${PROJECT_NAME}
)