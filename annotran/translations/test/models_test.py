# -*- coding: utf-8 -*-

from h import db
from h.test import factories
from h.groups import models as groups_models
from annotran.languages import models as lang_models
from annotran.pages import models as pages_models
from annotran.translations import models as tran_models

def test_init():
    p = pages_models.Page(uri="http://www.annotran_test.com/")
    db.Session.add(p)

    l = lang_models.Language(name="abc_language")
    db.Session.add(l)

    g = groups_models.Group(name="abc_group", creator=factories.User())
    db.Session.add(g)
    db.Session.flush()

    t = tran_models.Translation(page=p, language=l, group=g)
    db.Session.add(t)
    db.Session.flush()

    assert t.page_id == p.id
    assert t.group_id == g.id
    assert t.language_id == l.id

def test_get_by_composite_id():
    p = pages_models.Page(uri="http://www.annotran_test.com/")
    db.Session.add(p)

    l = lang_models.Language(name="abc_language")
    db.Session.add(l)

    g = groups_models.Group(name="abc_group", creator=factories.User())
    db.Session.add(g)
    db.Session.flush()

    t = tran_models.Translation(page=p, language=l, group=g)
    db.Session.add(t)
    db.Session.flush()

    assert tran_models.Translation.get_by_composite_id(p.id, l.id, g.id) == t

def test_get_translation_when_group_is_none():
    p = pages_models.Page(uri="http://www.annotran_test.com/")
    db.Session.add(p)

    l = lang_models.Language(name="abc_language")
    db.Session.add(l)

    g = groups_models.Group(name="Public", creator=factories.User())
    g.id = -1
    g.pubid = "__world__"
    db.Session.add(g)
    db.Session.flush()

    t = tran_models.Translation(page=p, language=l, group=g)
    db.Session.add(t)
    db.Session.flush()

    assert tran_models.Translation.get_translation(p, l, None) == t

def test_get_translation_when_group_is_not_none():
    p = pages_models.Page(uri="http://www.annotran_test.com/")
    db.Session.add(p)

    l = lang_models.Language(name="abc_language")
    db.Session.add(l)

    g = groups_models.Group(name="abc_group", creator=factories.User())
    db.Session.add(g)
    db.Session.flush()

    t = tran_models.Translation(page=p, language=l, group=g)
    db.Session.add(t)
    db.Session.flush()

    assert tran_models.Translation.get_translation(p, l, g) == t

def test_get_public_translations():
    p = pages_models.Page(uri="http://www.annotran_test.com/")
    db.Session.add(p)

    l1 = lang_models.Language(name="abc_language_1")
    db.Session.add(l1)

    l2 = lang_models.Language(name="abc_language_2")
    db.Session.add(l2)

    g = groups_models.Group(name="Public", creator=factories.User())
    g.id = -1
    g.pubid = "__world__"
    db.Session.add(g)
    db.Session.flush()

    t1 = tran_models.Translation(page=p, language=l1, group=g)
    t2 = tran_models.Translation(page=p, language=l2, group=g)
    db.Session.add(t1)
    db.Session.add(t2)
    db.Session.flush()

    assert tran_models.Translation.get_public_translations(p) ==  \
           [(l1.id, l1.name, l1.pubid, g.id), (l2.id, l2.name, l2.pubid, g.id)]

def test_get_public_translations_when_do_not_exist():
    p = pages_models.Page(uri="http://www.annotran_test.com/")
    db.Session.add(p)

    l1 = lang_models.Language(name="abc_language_1")
    db.Session.add(l1)

    l2 = lang_models.Language(name="abc_language_2")
    db.Session.add(l2)

    g = groups_models.Group(name="abc_group", creator=factories.User())
    db.Session.add(g)
    db.Session.flush()

    t1 = tran_models.Translation(page=p, language=l1, group=g)
    t2 = tran_models.Translation(page=p, language=l2, group=g)
    db.Session.add(t1)
    db.Session.add(t2)
    db.Session.flush()

    assert tran_models.Translation.get_public_translations(p) == []

def test_get_page_translations_with_single_group():
    p = pages_models.Page(uri="http://www.annotran_test.com/")
    db.Session.add(p)

    l1 = lang_models.Language(name="abc_language_1")
    db.Session.add(l1)

    l2 = lang_models.Language(name="abc_language_2")
    db.Session.add(l2)

    g = groups_models.Group(name="abc_group", creator=factories.User())
    db.Session.add(g)
    db.Session.flush()

    t1 = tran_models.Translation(page=p, language=l1, group=g)
    t2 = tran_models.Translation(page=p, language=l2, group=g)
    db.Session.add(t1)
    db.Session.add(t2)
    db.Session.flush()

    assert tran_models.Translation.get_page_translations(p) ==  \
           [(l1.id, l1.name, l1.pubid, g.id), (l2.id, l2.name, l2.pubid, g.id)]

def test_get_page_translations_with_multiple_groups():
    p = pages_models.Page(uri="http://www.annotran_test.com/")
    db.Session.add(p)

    l1 = lang_models.Language(name="abc_language_1")
    db.Session.add(l1)

    l2 = lang_models.Language(name="abc_language_2")
    db.Session.add(l2)

    l3 = lang_models.Language(name="abc_language_3")
    db.Session.add(l3)

    g1 = groups_models.Group(name="abc_group_1", creator=factories.User())
    db.Session.add(g1)
    db.Session.flush()

    g2 = groups_models.Group(name="abc_group_2", creator=factories.User())
    db.Session.add(g2)
    db.Session.flush()

    g3 = groups_models.Group(name="Public", creator=factories.User())
    g3.id = -1
    g3.pubid = "__world__"
    db.Session.add(g3)
    db.Session.flush()

    t1 = tran_models.Translation(page=p, language=l1, group=g1)
    t2 = tran_models.Translation(page=p, language=l2, group=g2)
    t3 = tran_models.Translation(page=p, language=l3, group=g3)
    db.Session.add(t1)
    db.Session.add(t2)
    db.Session.add(t3)
    db.Session.flush()

    assert tran_models.Translation.get_page_translations(p) ==  \
           [(l1.id, l1.name, l1.pubid, g1.id),
            (l2.id, l2.name, l2.pubid, g2.id),
            (l3.id, l3.name, l3.pubid, g3.id)]
