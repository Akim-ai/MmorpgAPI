import React from 'react'

export default class CreateAnnouncementForm extends React.Component {

    constructor(props) {
        super(props);
        this.category_choices = [
            'Танк', "Хил", "Демедж Диллер", "Торговец",
            "Гилдмастер", "Квестгивер", "Кузнец", "Кожевник",
            "Зельевар", "Мастер Заклинаний"
        ]

    }

    render(){ return (
         <div>
             <button onClick={this.props.openClose}>Отменить создание объявления</button>

                <form>
                    <h3>
                        Создать объявление
                    </h3>
                    <label htmlFor="announcement_title" >
                        Заголовок:
                        <input
                            onChange={this.props.onTitleChange}
                            id='announcement_title' type="text" value={this.props.title}
                        />
                    </label>


                    <label htmlFor="announcement_description">
                        Описание:
                        <input
                            onChange={this.props.onDescriptionChange}
                            type="text" id='announcement_description' value={this.props.description}
                        />
                    </label>

                    <label htmlFor="announcement_category">
                        Категория:
                        <select name="announcement_category" id="announcement_category"  value={this.props.category}
                                onChange={this.props.onCategoryChange}>
                            {this.category_choices.map((opt) => {
                                return <option value={opt}>{opt}</option>
                            })}
                        </select>
                    </label>
                    <button type='button' onClick={this.props.onSubmitForm}>Создать</button>
                </form>
            </div>
        )
    }
}