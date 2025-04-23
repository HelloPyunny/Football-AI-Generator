# edge_generator.py

from formation import get_line_info

def generate_edges_by_formation(formation_name, base_weight=1.0, reduced_weight=0.5):
    """
    FORMATIONS에 정의된 각 라인을 독립적인 라인으로 간주하여 엣지를 생성합니다.
    단, "GK" (골키퍼)는 엣지 연결에서 완전히 제외합니다.
    
    규칙:
    1. 각 라인 내에서는 인접한 노드끼리만 연결합니다.
    2. 서로 다른 라인 간에는 모든 노드 쌍을 연결합니다.
       - 인접한 라인(라인 차이가 1)은 기본 가중치(base_weight)
       - 인접하지 않은 라인은 낮은 가중치(reduced_weight)
       
    Args:
        formation_name (str): 예) "442", "433 (정석)", 등.
        base_weight (float): 인접한 라인끼리 연결 시 가중치 (기본값: 1.0)
        reduced_weight (float): 인접하지 않은 라인끼리 연결 시 가중치 (기본값: 0.5)
        
    Returns:
        edges (list): (node_from, node_to, weight) 형태의 튜플 리스트
    """
    edges = []
    formation_lines = get_line_info(formation_name)
    
    # Exclude GK
    filtered_lines = [line for line in formation_lines if not (len(line) == 1 and line[0] == "GK")]
    
    # 1. Connect nodes in same line
    for line in filtered_lines:
        if len(line) < 2:
            continue
        for i in range(len(line) - 1):
            node_from = line[i]
            node_to   = line[i+1]
            edges.append((node_from, node_to, base_weight))
    
    # 2. Connect nodes in different line
    n = len(filtered_lines)
    for i in range(n):
        for j in range(i+1, n):
            # if line diff = 1, base weight, else, reduced_weight
            weight = base_weight if (j - i) == 1 else reduced_weight
            for node_from in filtered_lines[i]:
                for node_to in filtered_lines[j]:
                    edges.append((node_from, node_to, weight))
    
    return edges

## TEST METHOD
if __name__ == "__main__":
    formation_name = "442"
    edges = generate_edges_by_formation(formation_name)
    print(f"포메이션 '{formation_name}'에 대해 생성된 엣지 (GK 제외):")
    for edge in edges:
        print(f"  {edge[0]} -> {edge[1]} (가중치: {edge[2]})")
