import csv
import math

_skill_resources_cache = None

def _load_skill_resources():
    global _skill_resources_cache
    if _skill_resources_cache is not None:
        return _skill_resources_cache
    
    _skill_resources_cache = {}
    try:
        with open('dataset/skill_resources.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                skill = row['skill'].strip().lower()
                _skill_resources_cache[skill] = {
                    'name': skill,
                    'category': row.get('category', ''),
                    'difficulty': row.get('difficulty', 'Intermediate'),
                    'prerequisite': row.get('prerequisite', '').strip().lower(),
                    'est_hours': int(row.get('est_hours', 15)),
                    'resource_title': row.get('resource_title', 'Search official documentation'),
                    'resource_url': row.get('resource_url', f'https://www.google.com/search?q={skill.replace(" ", "+")}+tutorial')
                }
    except Exception as e:
        print(f"Error loading skill_resources.csv: {e}")
        
    return _skill_resources_cache

def generate_roadmap(missing_skills, resume_skills, predicted_role, top_predictions=None, weekly_hours=10):
    resources = _load_skill_resources()
    
    # Normalize inputs
    missing = [s.strip().lower() for s in missing_skills]
    resume = [s.strip().lower() for s in resume_skills]
    
    # Get skill info for all missing skills
    skill_infos = {}
    for skill in missing:
        if skill in resources:
            skill_infos[skill] = resources[skill]
        else:
            skill_infos[skill] = {
                'name': skill,
                'category': 'Unknown',
                'difficulty': 'Intermediate',
                'prerequisite': '',
                'est_hours': 15,
                'resource_title': 'Search official documentation',
                'resource_url': f'https://www.google.com/search?q={skill.replace(" ", "+")}+tutorial'
            }

    # Calculate depth for each skill
    depths = {}
    
    def get_depth(skill, visited=None):
        if visited is None:
            visited = set()
        
        if skill in depths:
            return depths[skill]
            
        if skill in visited:
            return 1 # Cycle detected, break it
            
        visited.add(skill)
        
        prereq = skill_infos[skill]['prerequisite']
        
        # If no prereq, or prereq is already known by user, or prereq is not in missing list
        if not prereq or prereq in resume or prereq not in missing:
            depths[skill] = 1
            return 1
            
        # Recursive depth calculation
        d = 1 + get_depth(prereq, visited)
        depths[skill] = d
        return d
        
    for skill in missing:
        get_depth(skill)
        
    # Bucket skills by depth
    phase1_skills = []
    phase2_skills = []
    phase3_skills = []
    
    for skill in missing:
        d = depths[skill]
        info = skill_infos[skill]
        if d == 1:
            phase1_skills.append(info)
        elif d == 2:
            phase2_skills.append(info)
        else:
            phase3_skills.append(info)

    phases = []
    total_weeks = 0
    
    phase_definitions = [
        (1, "Foundation", phase1_skills),
        (2, "Core", phase2_skills),
        (3, "Advanced", phase3_skills)
    ]
    
    for phase_num, title, skills in phase_definitions:
        if skills:
            total_hours = sum(s['est_hours'] for s in skills)
            weeks = math.ceil(total_hours / weekly_hours)
            total_weeks += weeks
            
            formatted_skills = []
            for s in skills:
                formatted_skills.append({
                    "name": s["name"],
                    "hours": s["est_hours"],
                    "difficulty": s["difficulty"],
                    "resource_title": s["resource_title"],
                    "resource_url": s["resource_url"]
                })
                
            phases.append({
                "phase": phase_num,
                "title": title,
                "weeks": weeks,
                "skills": formatted_skills
            })

    return {
        "total_weeks": total_weeks,
        "weekly_hours": weekly_hours,
        "phases": phases
    }

if __name__ == "__main__":
    missing = ["docker", "kubernetes", "aws", "machine learning", "tensorflow"]
    resume = ["python", "linux"]
    predicted_role = "DevOps Engineer"
    
    roadmap = generate_roadmap(missing, resume, predicted_role, weekly_hours=10)
    
    print(f"Total Weeks: {roadmap['total_weeks']}")
    for p in roadmap['phases']:
        print(f"\nPhase {p['phase']}: {p['title']} ({p['weeks']} weeks)")
        for s in p['skills']:
            print(f" - {s['name']} ({s['hours']}h): {s['resource_title']}")

def render_roadmap_svg(roadmap_data):
    if not roadmap_data or not roadmap_data.get("phases"):
        return ""
    
    total_height = 40
    for phase in roadmap_data["phases"]:
        total_height += 60 + (len(phase.get("skills", [])) * 70)
        
    svg_parts = []
    svg_parts.append(f'<svg width="100%" height="auto" viewBox="0 0 800 {total_height}" xmlns="http://www.w3.org/2000/svg" style="background-color: transparent; font-family: system-ui, -apple-system, sans-serif;">')
    
    y_offset = 20
    colors = {1: "#e0e7ff", 2: "#dcfce7", 3: "#fef3c7"}
    border_colors = {1: "#c7d2fe", 2: "#bbf7d0", 3: "#fde68a"}
    
    for phase in roadmap_data["phases"]:
        phase_num = phase["phase"]
        bg_color = colors.get(phase_num, "#f3f4f6")
        bd_color = border_colors.get(phase_num, "#d1d5db")
        
        svg_parts.append(f'<g transform="translate(20, {y_offset})">')
        svg_parts.append(f'<text x="0" y="20" font-size="20" font-weight="bold" fill="#374151">{phase["title"]} Phase</text>')
        svg_parts.append(f'<text x="180" y="20" font-size="14" font-weight="normal" fill="#6b7280">({phase["weeks"]} Weeks)</text>')
        
        skill_y = 40
        for skill in phase["skills"]:
            svg_parts.append(f'<rect x="0" y="{skill_y}" width="760" height="55" rx="8" fill="{bg_color}" stroke="{bd_color}" stroke-width="1.5"/>')
            svg_parts.append(f'<text x="20" y="{skill_y + 32}" font-size="16" font-weight="600" fill="#1f2937" text-transform="capitalize">{skill["name"].title()}</text>')
            
            # Difficulty badge
            diff_color = "#22c55e" if skill["difficulty"] == "Beginner" else "#eab308" if skill["difficulty"] == "Intermediate" else "#ef4444"
            svg_parts.append(f'<rect x="250" y="{skill_y + 17}" width="90" height="22" rx="4" fill="{diff_color}" fill-opacity="0.1" stroke="{diff_color}" stroke-opacity="0.3"/>')
            svg_parts.append(f'<text x="295" y="{skill_y + 32}" font-size="12" font-weight="600" fill="{diff_color}" text-anchor="middle">{skill["difficulty"]}</text>')
            
            # Time
            svg_parts.append(f'<text x="380" y="{skill_y + 32}" font-size="14" fill="#4b5563">⏳ {skill["hours"]} hrs</text>')
            
            # Interactive toggle placeholder (visually)
            svg_parts.append(f'<g style="cursor: pointer;">')
            svg_parts.append(f'<rect x="630" y="{skill_y + 12}" width="110" height="30" rx="15" fill="#ffffff" stroke="#d1d5db" stroke-width="1"/>')
            svg_parts.append(f'<circle cx="645" cy="{skill_y + 27}" r="6" fill="#9ca3af"/>')
            svg_parts.append(f'<text x="660" y="{skill_y + 32}" font-size="13" font-weight="500" fill="#4b5563">Pending</text>')
            svg_parts.append('</g>')
            
            skill_y += 70
            
        y_offset += skill_y + 10
        svg_parts.append('</g>')
        
    svg_parts.append('</svg>')
    
    return "\n".join(svg_parts)
