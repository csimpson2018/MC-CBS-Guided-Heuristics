#pragma once
#include "CBSHeuristic.h"
#include "RectangleReasoning.h"
#include "CorridorReasoning.h"
#include "MutexReasoning.h"

#include <nlohmann/json.hpp>
#include <boost/filesystem.hpp>

#include <random>

enum class high_level_solver_type { ASTAR, ASTAREPS, NEW, EES, MCR };
enum class heuristic_guide {EPSILON, SOFTMAX, ZERO};

class CBS
{
public:
	bool randomRoot = false; // randomize the order of the agents in the root CT node

	/////////////////////////////////////////////////////////////////////////////////////
	// stats
	double runtime = 0;
	double runtime_generate_child = 0; // runtime of generating child nodes
	double runtime_build_CT = 0; // runtime of building constraint table
	double runtime_build_CAT = 0; // runtime of building conflict avoidance table
	double runtime_path_finding = 0; // runtime of finding paths for single agents
	double runtime_detect_conflicts = 0;
	double runtime_preprocessing = 0; // runtime of building heuristic table for the low level

	uint64_t num_cardinal_conflicts = 0;
	uint64_t num_corridor_conflicts = 0;
	uint64_t num_rectangle_conflicts = 0;
	uint64_t num_target_conflicts = 0;
	uint64_t num_mutex_conflicts = 0;
	uint64_t num_standard_conflicts = 0;

	uint64_t num_adopt_bypass = 0; // number of times when adopting bypasses

	uint64_t num_HL_expanded = 0;
	uint64_t num_HL_generated = 0;
	uint64_t num_LL_expanded = 0;
	uint64_t num_LL_generated = 0;

	uint64_t num_cleanup = 0; // number of expanded nodes chosen from cleanup list
	uint64_t num_open = 0; // number of expanded nodes chosen from open list
	uint64_t num_focal = 0; // number of expanded nodes chosen from focal list
	// CBSNode* dummy_start = nullptr;
	// CBSNode* goal_node = nullptr;
	HLNode* dummy_start = nullptr;
	HLNode* goal_node = nullptr;



	bool solution_found = false;
	int solution_cost = -2;

	/////////////////////////////////////////////////////////////////////////////////////////
	// set params
	void setHeuristicType(heuristics_type h, heuristics_type h_hat)
	{
	    heuristic_helper.type = h;
	    heuristic_helper.setInadmissibleHeuristics(h_hat);
	}
	void setPrioritizeConflicts(bool p) {PC = p;	heuristic_helper.PC = p; }
	void setRectangleReasoning(bool r) {rectangle_reasoning = r; heuristic_helper.rectangle_reasoning = r; }
	void setCorridorReasoning(bool c) {corridor_reasoning = c; heuristic_helper.corridor_reasoning = c; }
	void setTargetReasoning(bool t) {target_reasoning = t; heuristic_helper.target_reasoning = t; }
	void setMutexReasoning(bool m) {mutex_reasoning = m; heuristic_helper.mutex_reasoning = m; }
	void setDisjointSplitting(bool d) {disjoint_splitting = d; heuristic_helper.disjoint_splitting = d; }
	void setBypass(bool b) { bypass = b; } // 2-agent solver for heuristic calculation does not need bypass strategy.
	void setConflictSelectionRule(conflict_selection c) { conflict_selection_rule = c; heuristic_helper.conflict_seletion_rule = c; }
	void setNodeSelectionRule(node_selection n) { node_selection_rule = n; heuristic_helper.node_selection_rule = n; }
	void setSavingStats(bool s) { save_stats = s; heuristic_helper.save_stats = s; }
	void setHeuristicGuide(heuristic_guide g)
	{
		guide_type = g;
	}
	void setHighLevelSolver(high_level_solver_type s, double w)
	{
		solver_type = s;
		suboptimality = w;
	}
	void setNodeLimit(int n) { node_limit = n; }

	////////////////////////////////////////////////////////////////////////////////////////////
	// Runs the algorithm until the problem is solved or time is exhausted 
	bool solve(double time_limit, int cost_lowerbound = 0, int cost_upperbound = MAX_COST);

	int getLowerBound() const { return cost_lowerbound; }

	CBS(const Instance& instance, bool sipp, int screen, std::string jsonName);
	CBS(vector<SingleAgentSolver*>& search_engines,
		const vector<ConstraintTable>& constraints,
		vector<Path>& paths_found_initially, int screen);
	void clearSearchEngines();
	~CBS();

	// Save results
	void saveResults(const string &fileName, const string &instanceName);
	void saveStats(const string &fileName, const string &instanceName);
	void saveCT(const string &fileName) const; // write the CT to a file
    void savePaths(const string &fileName) const; // write the paths to a file
	void clear(); // used for rapid random  restart

	int getInitialPathLength(int agent) const {return (int) paths_found_initially[agent].size() - 1; }
protected:
    bool rectangle_reasoning;  // using rectangle reasoning
	bool corridor_reasoning;  // using corridor reasoning
	bool target_reasoning;  // using target reasoning
	bool disjoint_splitting;  // disjoint splitting
	bool mutex_reasoning;  // using mutex reasoning
	bool bypass; // using Bypass1
	bool PC; // prioritize conflicts
	bool save_stats;
	high_level_solver_type solver_type; // the solver for the high-level search
	heuristic_guide guide_type;
	conflict_selection conflict_selection_rule;
	node_selection node_selection_rule;

	MDDTable mdd_helper;	
	RectangleReasoning rectangle_helper;
	CorridorReasoning corridor_helper;
	MutexReasoning mutex_helper;
	CBSHeuristic heuristic_helper;

	list<HLNode*> allNodes_table; // this is ued for both ECBS and EES


	string getSolverName() const;

	int screen;
	
	double time_limit;
	double suboptimality = 1.0;
	int cost_lowerbound = 0;
	int inadmissible_cost_lowerbound;
	int node_limit = MAX_NODES;
	int cost_upperbound = MAX_COST;

	vector<ConstraintTable> initial_constraints;
	clock_t start;

	int num_of_agents;

	vector<int> solutionCosts;	// Sequentially tracks the solution costs every CT sample iteration

	vector<int> levelDeadCounts;	// Tracks the amount of dead ends in a CT level
	vector<int> levelGoalCounts;	// Tracks the amount of goal nodes in a CT level
	vector<int> levelNodeCounts;	// Tracks the amount of nodes in a CT level

	std::unordered_map<int, int> cost_goal_count_map;
	std::unordered_map<int, int> cost_dead_count_map;
	std::unordered_map<int, int> cost_level_count_map;

	std::string json_file_name;

	int sum_of_costs = 0;

	vector<Path*> paths;
	vector<Path> paths_found_initially;  // contain initial paths found
	// vector<MDD*> mdds_initially;  // contain initial paths found
	vector < SingleAgentSolver* > search_engines;  // used to find (single) agents' paths and mdd

	void addConstraints(const HLNode* curr, HLNode* child1, HLNode* child2) const;
	set<int> getInvalidAgents(const list<Constraint>& constraints); // return agents that violate the constraints
	//conflicts
	void findConflicts(HLNode& curr);
	void findConflicts(HLNode& curr, int a1, int a2);
	shared_ptr<Conflict> chooseConflict(const HLNode &node) const;
	static void copyConflicts(const list<shared_ptr<Conflict>>& conflicts,
		list<shared_ptr<Conflict>>& copy, const list<int>& excluded_agent) ;
	void removeLowPriorityConflicts(list<shared_ptr<Conflict>>& conflicts) const;
	void computeSecondPriorityForConflict(Conflict& conflict, const HLNode& node);

	inline void releaseNodes();

	// print and save
	void printResults() const;
	static void printConflicts(const HLNode &curr) ;

	bool validateSolution() const;
	inline int getAgentLocation(int agent_id, size_t timestep) const;

	vector<int> shuffleAgents() const;  //generate random permutation of agent indices
	bool terminate(HLNode* curr); // check the stop condition and return true if it meets
	void computeConflictPriority(shared_ptr<Conflict>& con, CBSNode& node); // check the conflict is cardinal, semi-cardinal or non-cardinal

	void getSOC(HLNode* node, vector<ConstraintTable> initial_constraints, vector<int> agents);

	void recordGoalNode(const HLNode* node);
	void recordDeadNode(const HLNode* node);
	void recordRegularNode(const HLNode* node);

	void writeJSON();


private: // CBS only, cannot be used by ECBS
	pairing_heap< CBSNode*, compare<CBSNode::compare_node_by_f> > cleanup_list; // it is called open list in ECBS
	pairing_heap< CBSNode*, compare<CBSNode::compare_node_by_inadmissible_f> > open_list; // this is used for EES
	pairing_heap< CBSNode*, compare<CBSNode::compare_node_by_d> > focal_list; // this is ued for both ECBS and EES

	// node operators
	inline void pushNode(CBSNode* node);
	CBSNode* selectNode();
	inline bool reinsertNode(CBSNode* node);

		 // high level search
	bool generateChild(CBSNode* child, CBSNode* curr);
	bool generateRoot();
	bool findPathForSingleAgent(CBSNode*  node, int ag, int lower_bound = 0);
	void classifyConflicts(CBSNode &parent);
		 //update information
	inline void updatePaths(CBSNode* curr);
	void printPaths() const;
};
