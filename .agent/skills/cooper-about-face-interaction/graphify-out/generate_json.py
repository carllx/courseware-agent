import json

nodes = [
    {
      "id": "about_face_chunks_chunk_576_context__context__context_context",
      "label": "Context",
      "file_type": "concept",
      "source_file": "chunk_576_Context__context__context.md",
      "source_location": None,
      "source_url": None,
      "captured_at": None,
      "author": None,
      "contributor": None
    },
    {
      "id": "about_face_chunks_chunk_577_shape_shape",
      "label": "Shape",
      "file_type": "concept",
      "source_file": "chunk_577_Shape.md",
      "source_location": None,
      "source_url": None,
      "captured_at": None,
      "author": None,
      "contributor": None
    },
    {
      "id": "about_face_chunks_chunk_578_size_size",
      "label": "Size",
      "file_type": "concept",
      "source_file": "chunk_578_Size.md",
      "source_location": None,
      "source_url": None,
      "captured_at": None,
      "author": None,
      "contributor": None
    },
    {
      "id": "about_face_chunks_chunk_579_color_color",
      "label": "Color",
      "file_type": "concept",
      "source_file": "chunk_579_Color.md",
      "source_location": None,
      "source_url": None,
      "captured_at": None,
      "author": None,
      "contributor": None
    },
    {
      "id": "about_face_chunks_chunk_580_value_value",
      "label": "Value",
      "file_type": "concept",
      "source_file": "chunk_580_Value.md",
      "source_location": None,
      "source_url": None,
      "captured_at": None,
      "author": None,
      "contributor": None
    },
    {
      "id": "about_face_chunks_chunk_581_hue_hue",
      "label": "Hue",
      "file_type": "concept",
      "source_file": "chunk_581_Hue.md",
      "source_location": None,
      "source_url": None,
      "captured_at": None,
      "author": None,
      "contributor": None
    },
    {
      "id": "about_face_chunks_chunk_582_saturation_saturation",
      "label": "Saturation",
      "file_type": "concept",
      "source_file": "chunk_582_Saturation.md",
      "source_location": None,
      "source_url": None,
      "captured_at": None,
      "author": None,
      "contributor": None
    },
    {
      "id": "about_face_chunks_chunk_583_hsv_in_combination_hsv",
      "label": "HSV Model",
      "file_type": "concept",
      "source_file": "chunk_583_HSV_in_combination.md",
      "source_location": None,
      "source_url": None,
      "captured_at": None,
      "author": None,
      "contributor": None
    },
    {
      "id": "about_face_chunks_chunk_584_orientation_orientation",
      "label": "Orientation",
      "file_type": "concept",
      "source_file": "chunk_584_Orientation.md",
      "source_location": None,
      "source_url": None,
      "captured_at": None,
      "author": None,
      "contributor": None
    },
    {
      "id": "about_face_chunks_chunk_585_texture_texture",
      "label": "Texture",
      "file_type": "concept",
      "source_file": "chunk_585_Texture.md",
      "source_location": None,
      "source_url": None,
      "captured_at": None,
      "author": None,
      "contributor": None
    },
    {
      "id": "about_face_chunks_chunk_586_position_position",
      "label": "Position",
      "file_type": "concept",
      "source_file": "chunk_586_Position.md",
      "source_location": None,
      "source_url": None,
      "captured_at": None,
      "author": None,
      "contributor": None
    },
    {
      "id": "about_face_chunks_chunk_587_text_and_typography_typography",
      "label": "Text and Typography",
      "file_type": "concept",
      "source_file": "chunk_587_Text_and_Typography.md",
      "source_location": None,
      "source_url": None,
      "captured_at": None,
      "author": None,
      "contributor": None
    },
    {
      "id": "about_face_chunks_chunk_588_information_hierarchy_information_hierarchy",
      "label": "Information Hierarchy",
      "file_type": "concept",
      "source_file": "chunk_588_Information_hierarchy.md",
      "source_location": None,
      "source_url": None,
      "captured_at": None,
      "author": None,
      "contributor": None
    },
    {
      "id": "about_face_chunks_chunk_589_motion_and_change_over_time_motion",
      "label": "Motion and change over time",
      "file_type": "concept",
      "source_file": "chunk_589_Motion_and_change_over_time.md",
      "source_location": None,
      "source_url": None,
      "captured_at": None,
      "author": None,
      "contributor": None
    },
    {
      "id": "about_face_chunks_chunk_590_visual_interface_design_princi_visual_interface_design",
      "label": "Visual Interface Design",
      "file_type": "concept",
      "source_file": "chunk_590_Visual_Interface_Design_Princi.md",
      "source_location": None,
      "source_url": None,
      "captured_at": None,
      "author": None,
      "contributor": None
    },
    {
      "id": "about_face_chunks_chunk_591_convey_a_tone_communicate_the__brand",
      "label": "Brand and Tone",
      "file_type": "concept",
      "source_file": "chunk_591_Convey_a_tone_communicate_the_.md",
      "source_location": None,
      "source_url": None,
      "captured_at": None,
      "author": None,
      "contributor": None
    },
    {
      "id": "about_face_chunks_chunk_592_lead_users_through_the_visual__visual_hierarchy",
      "label": "Visual Hierarchy",
      "file_type": "concept",
      "source_file": "chunk_592_Lead_users_through_the_visual_.md",
      "source_location": None,
      "source_url": None,
      "captured_at": None,
      "author": None,
      "contributor": None
    },
    {
      "id": "about_face_chunks_chunk_593_establish_relationships_relationships",
      "label": "Visual Relationships",
      "file_type": "concept",
      "source_file": "chunk_593_Establish_relationships.md",
      "source_location": None,
      "source_url": None,
      "captured_at": None,
      "author": None,
      "contributor": None
    },
    {
      "id": "about_face_chunks_chunk_594_occasionally__squint_at_it_squint_test",
      "label": "Squint Test",
      "file_type": "concept",
      "source_file": "chunk_594_Occasionally__squint_at_it.md",
      "source_location": None,
      "source_url": None,
      "captured_at": None,
      "author": None,
      "contributor": None
    },
    {
      "id": "about_face_chunks_chunk_595_provide_visual_structure_and_f_visual_structure",
      "label": "Visual Structure and Flow",
      "file_type": "concept",
      "source_file": "chunk_595_Provide_visual_structure_and_f.md",
      "source_location": None,
      "source_url": None,
      "captured_at": None,
      "author": None,
      "contributor": None
    },
    {
      "id": "about_face_chunks_chunk_596_align_to_a_grid_grid_system",
      "label": "Grid System",
      "file_type": "concept",
      "source_file": "chunk_596_Align_to_a_grid.md",
      "source_location": None,
      "source_url": None,
      "captured_at": None,
      "author": None,
      "contributor": None
    },
    {
      "id": "about_face_chunks_chunk_597_create_a_logical_path_logical_path",
      "label": "Logical Path",
      "file_type": "concept",
      "source_file": "chunk_597_Create_a_logical_path.md",
      "source_location": None,
      "source_url": None,
      "captured_at": None,
      "author": None,
      "contributor": None
    },
    {
      "id": "about_face_chunks_chunk_598_balance_the_interface_elements_balance",
      "label": "Asymmetrical Balance",
      "file_type": "concept",
      "source_file": "chunk_598_Balance_the_interface_elements.md",
      "source_location": None,
      "source_url": None,
      "captured_at": None,
      "author": None,
      "contributor": None
    },
    {
      "id": "about_face_chunks_chunk_599_signal_what_users_can_do_on_a__affordance",
      "label": "Affordance",
      "file_type": "concept",
      "source_file": "chunk_599_Signal_what_users_can_do_on_a_.md",
      "source_location": None,
      "source_url": None,
      "captured_at": None,
      "author": None,
      "contributor": None
    },
    {
      "id": "about_face_chunks_chunk_600_use_icons_icons",
      "label": "Icons",
      "file_type": "concept",
      "source_file": "chunk_600_Use_icons.md",
      "source_location": None,
      "source_url": None,
      "captured_at": None,
      "author": None,
      "contributor": None
    },
    {
      "id": "about_face_chunks_chunk_578_size_semiology_of_graphics",
      "label": "The Semiology of Graphics",
      "file_type": "document",
      "source_file": "chunk_578_Size.md",
      "source_location": None,
      "source_url": None,
      "captured_at": None,
      "author": "Jacques Bertin",
      "contributor": None
    },
    {
      "id": "about_face_chunks_chunk_600_use_icons_the_icon_book",
      "label": "The Icon Book",
      "file_type": "document",
      "source_file": "chunk_600_Use_icons.md",
      "source_location": None,
      "source_url": None,
      "captured_at": None,
      "author": "William Horton",
      "contributor": None
    }
]

edges = [
    {
      "source": "about_face_chunks_chunk_583_hsv_in_combination_hsv",
      "target": "about_face_chunks_chunk_581_hue_hue",
      "relation": "references",
      "confidence": "EXTRACTED",
      "confidence_score": 1.0,
      "source_file": "chunk_583_HSV_in_combination.md",
      "source_location": None,
      "weight": 1.0
    },
    {
      "source": "about_face_chunks_chunk_583_hsv_in_combination_hsv",
      "target": "about_face_chunks_chunk_582_saturation_saturation",
      "relation": "references",
      "confidence": "EXTRACTED",
      "confidence_score": 1.0,
      "source_file": "chunk_583_HSV_in_combination.md",
      "source_location": None,
      "weight": 1.0
    },
    {
      "source": "about_face_chunks_chunk_583_hsv_in_combination_hsv",
      "target": "about_face_chunks_chunk_580_value_value",
      "relation": "references",
      "confidence": "EXTRACTED",
      "confidence_score": 1.0,
      "source_file": "chunk_583_HSV_in_combination.md",
      "source_location": None,
      "weight": 1.0
    },
    {
      "source": "about_face_chunks_chunk_579_color_color",
      "target": "about_face_chunks_chunk_583_hsv_in_combination_hsv",
      "relation": "conceptually_related_to",
      "confidence": "EXTRACTED",
      "confidence_score": 1.0,
      "source_file": "chunk_579_Color.md",
      "source_location": None,
      "weight": 1.0
    },
    {
      "source": "about_face_chunks_chunk_590_visual_interface_design_princi_visual_interface_design",
      "target": "about_face_chunks_chunk_591_convey_a_tone_communicate_the__brand",
      "relation": "references",
      "confidence": "EXTRACTED",
      "confidence_score": 1.0,
      "source_file": "chunk_590_Visual_Interface_Design_Princi.md",
      "source_location": None,
      "weight": 1.0
    },
    {
      "source": "about_face_chunks_chunk_590_visual_interface_design_princi_visual_interface_design",
      "target": "about_face_chunks_chunk_592_lead_users_through_the_visual__visual_hierarchy",
      "relation": "references",
      "confidence": "EXTRACTED",
      "confidence_score": 1.0,
      "source_file": "chunk_590_Visual_Interface_Design_Princi.md",
      "source_location": None,
      "weight": 1.0
    },
    {
      "source": "about_face_chunks_chunk_590_visual_interface_design_princi_visual_interface_design",
      "target": "about_face_chunks_chunk_595_provide_visual_structure_and_f_visual_structure",
      "relation": "references",
      "confidence": "EXTRACTED",
      "confidence_score": 1.0,
      "source_file": "chunk_590_Visual_Interface_Design_Princi.md",
      "source_location": None,
      "weight": 1.0
    },
    {
      "source": "about_face_chunks_chunk_590_visual_interface_design_princi_visual_interface_design",
      "target": "about_face_chunks_chunk_599_signal_what_users_can_do_on_a__affordance",
      "relation": "references",
      "confidence": "EXTRACTED",
      "confidence_score": 1.0,
      "source_file": "chunk_590_Visual_Interface_Design_Princi.md",
      "source_location": None,
      "weight": 1.0
    },
    {
      "source": "about_face_chunks_chunk_578_size_size",
      "target": "about_face_chunks_chunk_578_size_semiology_of_graphics",
      "relation": "cites",
      "confidence": "EXTRACTED",
      "confidence_score": 1.0,
      "source_file": "chunk_578_Size.md",
      "source_location": None,
      "weight": 1.0
    },
    {
      "source": "about_face_chunks_chunk_600_use_icons_icons",
      "target": "about_face_chunks_chunk_600_use_icons_the_icon_book",
      "relation": "cites",
      "confidence": "EXTRACTED",
      "confidence_score": 1.0,
      "source_file": "chunk_600_Use_icons.md",
      "source_location": None,
      "weight": 1.0
    },
    {
      "source": "about_face_chunks_chunk_598_balance_the_interface_elements_balance",
      "target": "about_face_chunks_chunk_594_occasionally__squint_at_it_squint_test",
      "relation": "references",
      "confidence": "EXTRACTED",
      "confidence_score": 1.0,
      "source_file": "chunk_598_Balance_the_interface_elements.md",
      "source_location": None,
      "weight": 1.0
    },
    {
      "source": "about_face_chunks_chunk_599_signal_what_users_can_do_on_a__affordance",
      "target": "about_face_chunks_chunk_600_use_icons_icons",
      "relation": "references",
      "confidence": "INFERRED",
      "confidence_score": 0.85,
      "source_file": "chunk_599_Signal_what_users_can_do_on_a_.md",
      "source_location": None,
      "weight": 1.0
    }
]

out = {
  "nodes": nodes,
  "edges": edges,
  "hyperedges": [],
  "input_tokens": 0,
  "output_tokens": 0
}

with open("/tmp/about_face_chunks/graphify-out/.graphify_chunk_24.json", "w") as f:
    json.dump(out, f, indent=2)

print("Saved graph JSON.")
