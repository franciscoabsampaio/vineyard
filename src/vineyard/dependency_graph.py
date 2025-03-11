import matplotlib.pyplot as plt
import networkx as nx
import os
from typing import Self
from vineyard.io import DIRECTORY_OUTPUT, echo


class DependencyGraph(nx.DiGraph):
    def from_path_to_plans(self, path_to_plans: str) -> Self:
        """
        Scans all subfolders in the path_to_plans directory and builds a dependency graph.
        """
        for (root, _, files) in os.walk(path_to_plans, topdown=True):
            if "_deps.conf" in files:
                plan_name = root.split(path_to_plans)[-1].strip("/")
                self.add_node(plan_name)

                with open(f"{root}/_deps.conf", "r") as f:
                    dependencies = [line.strip() for line in f if (
                        line.strip()
                        and not line.startswith("#")  # Ignore comments
                    )]
                    for dependency in dependencies:
                        self.add_edge(dependency, plan_name)
        
        return self


    def save_to_png(self, target_directory: str = DIRECTORY_OUTPUT):
        plt.figure(figsize=(8, 5))
        nx.draw(self, with_labels=True, node_color="lightblue", edge_color="gray", arrowsize=20)
        plt.savefig(os.path.join(target_directory, "graph.png"), dpi=300)

        echo(f"graph.png was saved to {target_directory}.", log_level="INFO")


    def find_all_dependencies(self, node: str, visited=None) -> set:
        """
        Utility function to find all dependencies (parent nodes) recursively
        """

        if visited is None:
            visited = set()

        # Add the current node to the visited set
        visited.add(node)

        # Recursively find all dependencies (parents) of the current node
        for parent in self.predecessors(node):
            if parent not in visited:
                visited = self.find_all_dependencies(parent, visited)

        return visited


    def from_dependency_subgraph(self, node: str) -> Self:
        """
        Function to create a new DependencyGraph object from a subgraph, given a leaf node.
        
        args:
            node: The node where the dependency subgraph *ends*.
        """

        # Get all dependencies (parents) of the given node
        dependencies = self.find_all_dependencies(node)

        # Return the new dependency graph containing the node and its dependencies
        return self.subgraph(dependencies)
