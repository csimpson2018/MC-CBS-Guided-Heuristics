cmake_minimum_required (VERSION 3.11)

if(POLICY CMP0135) # This just fixes a warning
	cmake_policy(SET CMP0135 NEW)
	set(CMAKE_POLICY_DEFAULT_CMP0135 NEW)
endif()

project(CBSH2)

set(CMAKE_CXX_STANDARD 11)

SET(CMAKE_CXX_FLAGS  "${CMAKE_CXX_FLAGS} -g -Wall --std=c++0x")

include(FetchContent)

include_directories("inc")
file(GLOB SOURCES "*src/*.cpp")



# Find Boost
find_package( Boost 1.49.0 REQUIRED COMPONENTS program_options system filesystem)

# Download JSON
FetchContent_Declare(json URL https://github.com/nlohmann/json/releases/download/v3.11.3/json.tar.xz)
FetchContent_MakeAvailable(json)


include_directories( ${Boost_INCLUDE_DIRS})


add_executable(CBSH2 ${SOURCES} )
target_link_libraries(CBSH2 ${Boost_LIBRARIES} nlohmann_json::nlohmann_json)
