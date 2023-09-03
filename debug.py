import story_generation

failing_data = """
+++
Title: "Kyle's Quest for Vitality"
+++
Setting: The story unfolds in a mystical world named VitaLand, an enchanting realm that uniquely mirrors the real world with its serene landscapes, enchanted forests, enigmatic mountains, and magical rivers.
+++
Characters:
- Kyle: A brave 13-year-old boy who embarks on a great journey to overcome his challenges.
- Donald: Kyle's faithful guardian, a wise and caring figure who guides and protects Kyle along his path.
- King Dystro: The villain of the tale who masterfully manipulates elements of fear and symbolizes Kyle's illness.
- Arachnea: A menacing spider-like creature who embodies Kyle's deep fear of spiders, acting as King Dystro's henchman.
- Vitalia: A benevolent magical spirit who symbolizes hope and assists Kyle on his quest.

+++
Plot Points:
- Kyle enjoys a normal life in VitaLand until he starts experiencing mysterious fatigue and weakness hindering his usual activities.
- Donald reveals to Kyle about the existence of King Dystro, the remorseless villain causing Kyle's troubles.
- Kyle, along with Donald, decides to confront King Dystro to restore health and happiness to VitaLand.
- Journeying towards King Dystro's dark castle, the duo encounters a swarm of spiders led by Arachnea, forcing them to face Kyle's deepest fears.
- With courage, Kyle manages to overcome his fear of Arachnea and her spider swarm, marking his psychological victory.
- Kyle and Donald are aided by Vitalia, the spirit of hope, who gives them a shield of positivity to ward off Dystro's power.
- Vitalia guides Kyle to a magical river in VitaLand, where he can regain his strength by drinking its sparkling ether.
- Empowered and resolute, Kyle confronts King Dystro in a climactic struggle, emboldened by his triumph over his fears and his resolve to win.
- With his newfound strength and the help of Donald and Vitalia, Kyle is able to finally defeat King Dystro.
- King Dystro's defeat restores vitality to VitaLand and Kyle, symbolizing Kyle's regained health and strength, thereby marking the resolution of his journey.

"""

try:
    title, setting, characters = story_generation.extract_outline_data(failing_data)
    print('\n'.join(characters))
except Exception as e:
    print(f"Error in extract_outline_data: {e}")