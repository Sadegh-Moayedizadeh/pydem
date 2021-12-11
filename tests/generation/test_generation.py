from generation.container import Container


class TestGeneration:
    def test_no_contacts(self, kaolinite_dict, quartz_dict):
        kaolinite_dict["quantity"] = 500
        quartz_dict["quantity"] = 50
        container = Container(
            100000, 100000, [quartz_dict, kaolinite_dict], "tt", 0.01, {}
        )
        container.generate_particles()
        container.update_mechanical_boxes()
        container.update_mechanical_contacts_dictionary()
        print("////////")
        print(container.mechanical_contacts)
        contact_count = 0
        for p in container.mechanical_contacts.keys():
            contact_count += len(container.mechanical_contacts[p])
        assert contact_count == 0
