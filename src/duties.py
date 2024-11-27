""" Duty tasks """

from duty import duty
from duty.context import Context


@duty
def translations(ctx: Context):
    """ Update translation """

    ctx.run('pybabel extract . -o resources/locales/base.po')
    ctx.run('pybabel update -i resources/locales/base.pot -d resources/locales')
    ctx.run('pybabel compile -d resources/locales --use-fuzzy')


@duty
def optimize(ctx: Context):
    """ Optimize images """

    print(ctx.run('optimize-images .'))


def pylint(ctx: Context):
    """ Lint  code """

    print(ctx.run('pylint .'))
