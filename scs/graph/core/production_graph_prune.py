class NetworkXGraphPrune:
    def prune_singleton_produced_items(self):
        to_remove = []
        for node in list(self.nx.node_ids):
            node_data = self.nx.node_ids[node].get("data")
            # Only consider nodes representing an ItemORM that is produced.
            if isinstance(node_data, Item):
                in_edges = list(self.nx.in_edges(node, data="weight"))
                out_edges = list(self.nx.out_edges(node, data="weight"))
                # Only prune produced items with exactly one incoming and one outgoing edge, both with weight 1.
                if len(in_edges) == 1 and len(out_edges) == 1:
                    if in_edges[0][2] == 1 and out_edges[0][2] == 1:
                        pred = in_edges[0][0]
                        succ = out_edges[0][1]
                        # Reconnect predecessor to successor.
                        self.nx._add_edge(pred, succ, weight=1)
                        to_remove.append(node)
        self.nx.remove_nodes_from(to_remove)
